from pathlib import Path
from xml.etree import ElementTree as ET

from TARgET.core.base.tree import AbstractTree
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.base.symbol import Ranked_Symbol


class TreeXMLImporter:
    """Import tree structures from XML."""

    @staticmethod
    def import_tree(filepath: str | Path) -> RankedTree:
        """Import a ranked tree from an XML file."""

        xml_tree = ET.parse(filepath)
        root = xml_tree.getroot()

        if root.tag != "tree":
            raise ValueError("Invalid XML tree format")

        tree_type = root.get("type")

        if tree_type != "ranked":
            raise ValueError(
                f"Unsupported tree type: {tree_type}"
            )

        node = root.find("node")

        if node is None:
            raise ValueError("XML file contains no tree node")

        return TreeXMLImporter._element_to_tree(node)

    @staticmethod
    def _element_to_tree(element: ET.Element) -> RankedTree:
        """Convert an XML node into a RankedTree."""

        symbol_name = element.get("symbol")
        rank = element.get("rank")

        if symbol_name is None or rank is None:
            raise ValueError(
                "Each ranked tree node must define "
                "'symbol' and 'rank'"
            )

        symbol = Ranked_Symbol(
            name=symbol_name,
            rank=int(rank)
        )

        tree = RankedTree(symbol)

        for child_element in element:
            child = TreeXMLImporter._element_to_tree(child_element)
            tree.add_child(child)

        if not tree.is_well_formed():
            raise ValueError(
                f"Node '{symbol_name}' has an invalid number of children"
            )

        return tree

# Example usage

if __name__ == "__main__":
    tree = TreeXMLImporter.import_tree("tree.xml")

    print(tree)
    print(tree.is_well_formed())