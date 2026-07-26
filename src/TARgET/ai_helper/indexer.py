from dataclasses import dataclass, field
from typing import List, Optional
import ast
from pathlib import Path


"""
This module indexes a Python codebase by extracting source-code units such as
modules, classes, methods, and functions.

Each SemanticUnit stores both structural metadata and the actual source code.
The source code is later used by the semantic retriever and provided to the
language model as context.

The indexer recursively processes Python files while skipping common noise
directories such as virtual environments, caches, version-control directories,
and build artifacts.
"""


IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "venv",
    ".venv",
    "env",
    ".env",
    "virtualenv",
    "node_modules",
    "build",
    "dist",
    ".tox",
    ".idea",
    ".vscode",
}


@dataclass
class SemanticUnit:
    """
    Represents a source-code unit extracted from a Python codebase.

    A unit can be a module, class, method, or function. In addition to its
    semantic metadata, it stores the actual source code so that retrieval can
    provide the language model with implementation details rather than only
    documentation.
    """

    kind: str
    name: str
    file: str
    signature: str
    docstring: str
    code: str

    bases: List[str] = field(default_factory=list)
    parent: Optional[str] = None

    module: Optional[str] = None
    decorators: List[str] = field(default_factory=list)

    start_line: Optional[int] = None
    end_line: Optional[int] = None


def _get_name(node: ast.AST) -> str:
    """
    Converts an AST expression into a readable name.

    This supports names such as:

        Foo
        module.Foo
        typing.Generic[T]
    """

    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _build_signature(node: ast.AST) -> str:
    """
    Builds a source-like signature for a function or method.
    """

    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"

    args = ast.unparse(node.args)

    returns = ""
    if node.returns is not None:
        returns = f" -> {ast.unparse(node.returns)}"

    return f"{prefix} {node.name}({args}){returns}"


def _get_decorators(node: ast.AST) -> List[str]:
    """
    Returns decorators applied to a class or function.
    """

    return [
        ast.unparse(decorator)
        for decorator in getattr(node, "decorator_list", [])
    ]


def _function_unit(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    path: Path,
    source: str,
    kind: str,
    module: str,
    parent: Optional[str] = None,
) -> SemanticUnit:
    """
    Builds a SemanticUnit for a function or method.
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
        module=module,
        decorators=_get_decorators(node),
        start_line=node.lineno,
        end_line=getattr(node, "end_lineno", None),
    )


def _class_unit(
    node: ast.ClassDef,
    path: Path,
    source: str,
    module: str,
    parent: Optional[str] = None,
) -> SemanticUnit:
    """
    Builds a SemanticUnit for a class.
    """

    bases = [_get_name(base) for base in node.bases]

    base_text = f"({', '.join(bases)})" if bases else ""

    return SemanticUnit(
        kind="class",
        name=node.name,
        file=str(path),
        signature=f"class {node.name}{base_text}",
        docstring=ast.get_docstring(node) or "",
        code=ast.get_source_segment(source, node) or "",
        bases=bases,
        parent=parent,
        module=module,
        decorators=_get_decorators(node),
        start_line=node.lineno,
        end_line=getattr(node, "end_lineno", None),
    )


def _extract_class_units(
    node: ast.ClassDef,
    path: Path,
    source: str,
    module: str,
    parent: Optional[str] = None,
) -> List[SemanticUnit]:
    """
    Extracts a class and its methods.

    Nested classes are also recursively indexed.
    """

    units = []

    class_name = (
        f"{parent}.{node.name}"
        if parent
        else node.name
    )

    units.append(
        _class_unit(
            node=node,
            path=path,
            source=source,
            module=module,
            parent=parent,
        )
    )

    for child in node.body:

        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            units.append(
                _function_unit(
                    node=child,
                    path=path,
                    source=source,
                    kind="method",
                    module=module,
                    parent=class_name,
                )
            )

        elif isinstance(child, ast.ClassDef):
            units.extend(
                _extract_class_units(
                    node=child,
                    path=path,
                    source=source,
                    module=module,
                    parent=class_name,
                )
            )

    return units


def extract_units_from_file(path: Path) -> List[SemanticUnit]:
    """
    Extracts source-code units from one Python file.

    The extracted units include:

    - the module;
    - top-level classes;
    - methods;
    - nested classes;
    - top-level functions;
    - async functions and methods.
    """

    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        # Ignore files that cannot be parsed.
        return []

    units: List[SemanticUnit] = []

    module_name = path.stem

    module_docstring = ast.get_docstring(tree)

    units.append(
        SemanticUnit(
            kind="module",
            name=module_name,
            file=str(path),
            signature=f"module {module_name}",
            docstring=module_docstring or "",
            code=source,
            module=module_name,
            start_line=1,
            end_line=len(source.splitlines()),
        )
    )

    for node in tree.body:

        if isinstance(node, ast.ClassDef):
            units.extend(
                _extract_class_units(
                    node=node,
                    path=path,
                    source=source,
                    module=module_name,
                )
            )

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            units.append(
                _function_unit(
                    node=node,
                    path=path,
                    source=source,
                    kind="function",
                    module=module_name,
                )
            )

    return units


def index_toolkit(toolkit_path: str) -> List[SemanticUnit]:
    """
    Recursively indexes all Python files in a toolkit.
    """

    all_units: List[SemanticUnit] = []

    root = Path(toolkit_path)

    for py_file in root.rglob("*.py"):

        if any(
            part in IGNORED_DIR_NAMES
            for part in py_file.parts
        ):
            continue

        all_units.extend(
            extract_units_from_file(py_file)
        )

    return all_units


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."

    units = index_toolkit(target)

    print(
        f"Indexed {len(units)} units from {target}\n"
    )

    for unit in units[:5]:

        print(
            f"[{unit.kind}] "
            f"{unit.name} "
            f"({unit.file})"
        )

        print(
            f"  {unit.signature}"
        )

        if unit.parent:
            print(
                f"  parent: {unit.parent}"
            )

        print(
            f"  lines: "
            f"{unit.start_line}-"
            f"{unit.end_line}"
        )

        print()