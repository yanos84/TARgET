from dataclasses import dataclass
from typing import List
import ast
from pathlib import Path

@dataclass
class SemanticUnit:
    kind: str               # "class" | "function"
    name: str
    file: str
    signature: str
    docstring: str
    code: str
    bases: List[str]


import ast
from pathlib import Path

def extract_units_from_file(path: Path) -> list[SemanticUnit]:
    source = path.read_text()
    tree = ast.parse(source)
    units = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]

            units.append(
                SemanticUnit(
                    kind="class",
                    name=node.name,
                    file=str(path),
                    signature=f"class {node.name}({', '.join(bases)})",
                    docstring=doc,
                    code=ast.get_source_segment(source, node),
                    bases=bases
                )
            )

        elif isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node) or ""
            units.append(
                SemanticUnit(
                    kind="function",
                    name=node.name,
                    file=str(path),
                    signature=f"def {node.name}(...)",
                    docstring=doc,
                    code=ast.get_source_segment(source, node),
                    bases=[]
                )
            )

    return units


def extract_units_from_file(path: Path) -> list[SemanticUnit]:
    source = path.read_text()
    tree = ast.parse(source)
    units = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            bases = [b.id for b in node.bases if isinstance(b, ast.Name)]

            units.append(
                SemanticUnit(
                    kind="class",
                    name=node.name,
                    file=str(path),
                    signature=f"class {node.name}({', '.join(bases)})",
                    docstring=doc,
                    code=ast.get_source_segment(source, node),
                    bases=bases
                )
            )

        elif isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node) or ""
            units.append(
                SemanticUnit(
                    kind="function",
                    name=node.name,
                    file=str(path),
                    signature=f"def {node.name}(...)",
                    docstring=doc,
                    code=ast.get_source_segment(source, node),
                    bases=[]
                )
            )

    return units


def index_toolkit(toolkit_path: str) -> list[SemanticUnit]:
    all_units = []
    for py_file in Path(toolkit_path).rglob("*.py"):
        all_units.extend(extract_units_from_file(py_file))
    return all_units


if __name__ == "__main__":
    units = index_toolkit("/run/media/yanos/48D8EB77D8EB6224/Python_projects/TARgET")
    print(len(units))
    print(units[0])
