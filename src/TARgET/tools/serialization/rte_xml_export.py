from pathlib import Path
from xml.etree import ElementTree as ET
from TARgET.core.rte.rte import Rte, Zero, One, Atom, function, Plus, CProduct, CStar
from TARgET.core.base.symbol import Symbol, Ranked_Symbol

"""
    XML exporter for Rational Tree Expressions.
    Produces the XML representation of RTEs for serialization and storage.
    Example usage is provided at the end of this file.
    It prodcues the following XML for the example RTE:
    <?xml version='1.0' encoding='utf-8'?>
<rte>
    <plus>
        <cproduct concat="a">
            <function symbol="f" rank="2">
                <atom symbol="a" rank="0" />
                <atom symbol="b" rank="0" />
            </function>
            <function symbol="g" rank="1">
                <atom symbol="x" rank="0" />
            </function>
        </cproduct>
        <cstar concat="b">
            <function symbol="f" rank="2">
                <atom symbol="a" rank="0" />
                <atom symbol="b" rank="0" />
            </function>
        </cstar>
    </plus>
</rte>
"""

class RteXMLExporter:
    """
    Export Rational Tree Expressions to XML.
    """

    @staticmethod
    def export(rte: Rte, filepath: str | Path):
        """
        Export an RTE into an XML file.

        Parameters
        ----------
        rte:
            The RTE to export.

        filepath:
            Destination XML file.
        """

        if not isinstance(rte, Rte):
            raise TypeError(
                "Only Rte instances can be exported"
            )

        root = ET.Element("rte")

        root.append(
            RteXMLExporter._rte_to_element(rte)
        )

        tree = ET.ElementTree(root)

        ET.indent(tree, space="    ")

        tree.write(
            filepath,
            encoding="utf-8",
            xml_declaration=True
        )


    @staticmethod
    def _rte_to_element(rte: Rte) -> ET.Element:
        """
        Convert an RTE object into an XML element.
        """


        # -----------------------------
        # Zero
        # -----------------------------
        if isinstance(rte, Zero):
            return ET.Element("zero")


        # -----------------------------
        # One
        # -----------------------------
        if isinstance(rte, One):
            return ET.Element("one")


        # -----------------------------
        # Atom
        # -----------------------------
        if isinstance(rte, Atom):

            element = ET.Element(
                "atom",
                {
                    "symbol": rte.symbol.name
                }
            )

            if isinstance(
                rte.symbol,
                Ranked_Symbol
            ):
                element.set(
                    "rank",
                    str(rte.symbol.rank)
                )

            return element


        # -----------------------------
        # Function
        # -----------------------------
        if isinstance(rte, function):

            element = ET.Element(
                "function",
                {
                    "symbol": rte.symbol.name
                }
            )

            if isinstance(
                rte.symbol,
                Ranked_Symbol
            ):
                element.set(
                    "rank",
                    str(rte.symbol.rank)
                )


            if rte.args is not None:

                for arg in rte.args:

                    element.append(
                        RteXMLExporter._rte_to_element(arg)
                    )

            return element


        # -----------------------------
        # Plus
        # -----------------------------
        if isinstance(rte, Plus):

            element = ET.Element("plus")

            for term in rte.terms:

                element.append(
                    RteXMLExporter._rte_to_element(term)
                )

            return element


        # -----------------------------
        # CProduct
        # -----------------------------
        if isinstance(rte, CProduct):

            element = ET.Element(
                "cproduct",
                {
                    "concat": rte.concat
                }
            )

            element.append(
                RteXMLExporter._rte_to_element(rte.left)
            )

            element.append(
                RteXMLExporter._rte_to_element(rte.right)
            )

            return element


        # -----------------------------
        # CStar
        # -----------------------------
        if isinstance(rte, CStar):

            element = ET.Element(
                "cstar",
                {
                    "concat": rte.concat.name
                }
            )

            element.append(
                RteXMLExporter._rte_to_element(rte.expr)
            )

            return element


        raise TypeError(
            f"Unsupported RTE type: {type(rte)}"
        )
# Example usage:

if __name__ == "__main__":
    a, b, x, f, g = Ranked_Symbol("a"), Ranked_Symbol("b"), Ranked_Symbol("x"), Ranked_Symbol("f", 2), Ranked_Symbol("g", 1)
    Ea, Eb, Ex = Atom(a), Atom(b), Atom(x)
    # trees
    fab = function(f, [Ea, Eb])
    gx  = function(g, [Ex])
    # rational tree expression
    rte = Plus(
        CStar(fab, b),
        CProduct(fab, gx, a)
    )
    print(rte)
    RteXMLExporter.export(
    rte,
    "example_rte.xml"
)