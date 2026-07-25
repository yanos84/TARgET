from pathlib import Path
from xml.etree import ElementTree as ET

from TARgET.core.base.tree import AbstractTree
from TARgET.core.base.rankedTree import RankedTree


class TreeXMLExporter:
    """Export tree structures to XML."""

    @staticmethod
    def export(tree: AbstractTree, filepath: str | Path) -> None:
        """Export a tree to an XML file.

        Args:
            tree: The tree to export.
            filepath: Destination XML file.

        Raises:
            TypeError: If ``tree`` is not an AbstractTree.
            ValueError: If a ranked tree is not well-formed.
        """
        if not isinstance(tree, AbstractTree):
            raise TypeError("tree must be an instance of AbstractTree")

        if isinstance(tree, RankedTree) and not tree.is_well_formed():
            raise ValueError("Cannot export an ill-formed ranked tree")

        root = ET.Element("tree")

        if isinstance(tree, RankedTree):
            root.set("type", "ranked")
        else:
            root.set("type", "abstract")

        root.append(TreeXMLExporter._tree_to_element(tree))

        xml_tree = ET.ElementTree(root)

        ET.indent(xml_tree, space="    ")

        xml_tree.write(
            filepath,
            encoding="utf-8",
            xml_declaration=True
        )

    @staticmethod
    def _tree_to_element(tree: AbstractTree) -> ET.Element:
        """Convert a tree node into an XML element."""

        if isinstance(tree, RankedTree):
            element = ET.Element(
                "node",
                {
                    "symbol": tree.ranked_symbol.name,
                    "rank": str(tree.ranked_symbol.rank),
                }
            )
        else:
            element = ET.Element(
                "node",
                {
                    "symbol": tree.symbol,
                }
            )

        for child in tree.children:
            element.append(TreeXMLExporter._tree_to_element(child))

        return element

# Example of use

if __name__ == "__main__":
    from TARgET.core.base.symbol import Ranked_Symbol

    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)
    root = RankedTree(f)
    root.add_child(RankedTree(a))
    root.add_child(RankedTree(a))

    TreeXMLExporter.export(root, "tree.xml") 