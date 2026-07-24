from ..rte import Rte, Zero, One, Atom, function, CStar, CProduct, Plus
from ...algebraic.semiring import Semiring

class WeightedRtePrinter:
    """
    A class for printing weighted rational tree expressions (RTEs) with associated weights. The class takes a dictionary of weights for symbols and provides a method to print the RTE in a human-readable format, including the weights of the symbols. The weights are represented using a semiring structure, allowing for various algebraic operations on the weights. The `print` method recursively traverses the RTE structure and formats the output accordingly, handling different types of RTEs such as Zero, One, Atom, function, Plus, CProduct, and CStar.
    """
    def __init__(self, weights: dict[str, Semiring]):
        """
        Initializes the WeightedRtePrinter with a dictionary of weights for symbols.
        :param weights: A dictionary mapping symbol names to their corresponding weights (Semiring elements).
        """
        self.weights = weights
    
    def print(self, rte: Rte, global_weight = None) -> str:
        """
        Recursively prints the weighted rational tree expression (RTE) in a human-readable format, including the weights of the symbols.
        :param rte: The rational tree expression (RTE) to be printed.
        :param global_weight: An optional global weight to be applied to the entire RTE (default is None).
        :return: A string representation of the weighted RTE.
        """
        if global_weight !=None:
            return f"{global_weight}{self.print(rte)}"
        else:

            if isinstance(rte, (Zero, One)):
                return f"{rte}"
            if isinstance(rte, Atom):
                w= self.weights[rte.symbol.name]
                return f"{w} ⊗ {rte}"
            if isinstance(rte, function):
                args = ", ".join(self.print(a) for a in rte.args)
                return f"{rte.symbol.name}({args})"
            if isinstance(rte, Plus):
                return " + ".join(self.print(t) for t in rte.terms)
            if isinstance(rte, CProduct):
                return f"{self.print(rte.left)}.{rte.concat}{self.print(rte.left)}"
            if isinstance(rte, CStar):
                return f"{self.print(rte.expr)}*{rte.concat.name}"


