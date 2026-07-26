from dataclasses import dataclass, field
from typing import List, Optional
import ast
from pathlib import Path

"""
This module provides functionality for indexing a codebase by extracting semantic units:
modules, classes, methods, and functions. It defines a SemanticUnit dataclass to represent
these units, including their kind, name, file location, real signature, docstring, code,
base classes (for classes), and parent (for methods). The module includes functions to
extract semantic units from individual Python files and to index an entire toolkit by
recursively processing all Python files in a specified directory, skipping common noise
directories (virtual envs, caches, VCS folders). This indexed information is intended to
be fed into an LLM to help contributors understand and extend the toolkit.
"""

# Directories we never want to walk into when indexing a project.
IGNORED_DIR_NAMES = {
    ".git", ".hg", ".svn",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "venv", ".venv", "env", ".env", "virtualenv",
    "node_modules", "build", "dist", ".tox", ".idea", ".vscode",
}


@dataclass
class SemanticUnit:
    """
    Represents a module, class, method, or function in the codebase, capturing its
    essential information for indexing and retrieval.
    """
    kind: str                      # "module" | "class" | "method" | "function"
    name: str
    file: str
    signature: str
    docstring: str
    code: str
    bases: List[str] = field(default_factory=list)   # populated for classes
    parent: Optional[str] = None                       # populated for methods (owning class name)


def _build_signature(node: ast.AST) -> str:
    """
    Builds a real signature string (e.g. "def foo(a, b=1, *args) -> int") for a
    FunctionDef or AsyncFunctionDef node, instead of a generic placeholder.
    """
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    args_str = ast.unparse(node.args)
    returns_str = f" -> {ast.unparse(node.returns)}" if node.returns is not None else ""
    return f"{prefix} {node.name}({args_str}){returns_str}"


def _function_unit(node, path: Path, source: str, kind: str, parent: Optional[str] = None) -> SemanticUnit:
    """
    Builds a SemanticUnit for a function or method node. `kind` should be
    "function" for top-level defs and "method" for defs nested inside a class.
    """
    return SemanticUnit(
        kind=kind,
        name=node.name,
        file=str(path),
        signature=_build_signature(node),
        docstring=ast.get_docstring(node) or "",
        code=ast.get_source_segment(source, node) or "",
        bases=[],
        parent=parent,
    )


def extract_units_from_file(path: Path) -> List[SemanticUnit]:
    """
    Extracts semantic units (module docstring, classes, methods, and top-level
    functions -- sync or async) from a given Python file.
    """
    source = path.read_text()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Skip files that don't parse (e.g. Python 2 leftovers, corrupted files)
        return []

    units: List[SemanticUnit] = []

    module_doc = ast.get_docstring(tree)
    if module_doc:
        units.append(
            SemanticUnit(
                kind="module",
                name=path.stem,
                file=str(path),
                signature=f"module {path.stem}",
                docstring=module_doc,
                code="",
                bases=[],
            )
        )

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]

            units.append(
                SemanticUnit(
                    kind="class",
                    name=node.name,
                    file=str(path),
                    signature=f"class {node.name}({', '.join(bases)})",
                    docstring=ast.get_docstring(node) or "",
                    code=ast.get_source_segment(source, node) or "",
                    bases=bases,
                )
            )

            # Walk the class body (not the whole tree) so we only pick up its
            # own methods, not functions nested inside other functions/classes.
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    units.append(_function_unit(child, path, source, kind="method", parent=node.name))

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            units.append(_function_unit(node, path, source, kind="function"))

    return units


def index_toolkit(toolkit_path: str) -> List[SemanticUnit]:
    """
    Indexes all Python files in the given toolkit path, extracting semantic units
    from each file. Skips common noise directories (virtual envs, VCS folders,
    caches, build artifacts) so they don't pollute retrieval results.
    """
    all_units: List[SemanticUnit] = []
    root = Path(toolkit_path)

    for py_file in root.rglob("*.py"):
        if any(part in IGNORED_DIR_NAMES for part in py_file.parts):
            continue
        all_units.extend(extract_units_from_file(py_file))

    return all_units


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    units = index_toolkit(target)
    print(f"Indexed {len(units)} units from {target}\n")
    for u in units[:5]:
        print(f"[{u.kind}] {u.name}  ({u.file})")
        print(f"  {u.signature}")
        if u.parent:
            print(f"  parent: {u.parent}")
        print()