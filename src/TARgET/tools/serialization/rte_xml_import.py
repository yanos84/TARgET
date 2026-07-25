from pathlib import Path
from xml.etree import ElementTree as ET
from TARgET.core.rte.rte import Rte, Zero, One, Atom, function, Plus, CProduct, CStar
from TARgET.core.base.symbol import Symbol, Ranked_Symbol

class RteXMLImporter:
    """
    Import Rational Tree Expressions from XML.
    """


    @staticmethod
    def import_rte(filepath: str | Path) -> Rte:
        """
        Import an RTE from an XML file.
        """

        tree = ET.parse(filepath)
        root = tree.getroot()
        if root.tag != "rte":
            raise ValueError(
                "Invalid XML format: expected <rte>"
            )

        element = root.find("*")
        if element is None:
            raise ValueError(
                "Empty RTE XML document"
            )
        return RteXMLImporter._element_to_rte(element)

    @staticmethod
    def _element_to_rte(element: ET.Element) -> Rte:
        """
        Convert an XML element into an RTE object.
     """

        if element.tag == "zero":
            return Zero()

        if element.tag == "one":
            return One()

        if element.tag == "atom":
            symbol = (
                RteXMLImporter._parse_symbol(element)
            )
            return Atom(symbol)


        if element.tag == "function":
            symbol = (
                RteXMLImporter._parse_symbol(element)
            )
            args = [
                RteXMLImporter._element_to_rte(child)
                for child in element
            ]


            return function(symbol,args)

        if element.tag == "plus":
            terms = [
                RteXMLImporter._element_to_rte(child)
                for child in element
            ]


            return Plus(
                *terms
            )

        if element.tag == "cproduct":
            children = list(element)
            if len(children) != 2:
                raise ValueError(
                    "CProduct requires two operands"
                )
            concat = element.get(
                "concat"
            )
            if concat is None:
                raise ValueError(
                    "Missing concat attribute"
                )
            left = (
                RteXMLImporter._element_to_rte(
                    children[0]
                )
            )
            right = (
                RteXMLImporter._element_to_rte(
                    children[1]
                )
            )
            return CProduct(
                left,
                right,
                Symbol(concat)
            )

        if element.tag == "cstar":
            children = list(element)
            if len(children) != 1:
                raise ValueError(
                    "CStar requires one operand"
                )
            concat = element.get(
                "concat"
            )
            if concat is None:

                raise ValueError(
                    "Missing concat attribute"
                )
            expr = (
                RteXMLImporter._element_to_rte(
                    children[0]
                )
            )
            return CStar(
                expr,
                Symbol(concat)
            )
        raise ValueError(
            f"Unknown RTE XML element: {element.tag}"
        )
    @staticmethod
    def _parse_symbol(element: ET.Element) -> Symbol:
        """
        Reconstruct a Symbol or Ranked_Symbol
        from XML attributes.
        """
        name = element.get(
            "symbol"
        )
        if name is None:

            raise ValueError(
                "Missing symbol attribute"
            )
        rank = element.get(
            "rank"
        )
        if rank is not None:

            return Ranked_Symbol(
                name,
                int(rank)
            )
        return Symbol(name)

# Example usage:
if __name__ == "__main__":
    rte = RteXMLImporter.import_rte("example_rte.xml")
    print(rte)