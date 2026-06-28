from TARgET.rte.rte import Rte
from TARgET.algebric.semiring import Semiring

class Weight(Rte):
    """
    Represents k ⊗ E
    where k is a weight from a semiring and E is a rational tree expression (RTE).
    This class allows for the representation of weighted rational tree expressions, where the weight is associated with the RTE. The weight is an element of a semiring, enabling various algebraic operations on
    """
    def __init__(self, weight: Semiring, expr: Rte):
        """
        Initializes a Weight object with a given weight and rational tree expression (RTE).
        :param weight: A weight from a semiring (Semiring element).
        :param expr: A rational tree expression (RTE) to be associated with the weight.
        """
        self.weight = weight
        self.expr = expr

    def __str__(self):
        """
        Returns a string representation of the weighted rational tree expression (RTE) in the form "k ⊗ (E)".
        :return: A string representing the weighted RTE.
        """
        return f"{self.weight} ⊗ ({self.expr})"

    def _key(self):
        """
        Returns a tuple representing the key for the weighted rational tree expression (RTE), which includes the weight and the key of the associated RTE.
        :return: A tuple containing the weight and the key of the associated RTE.
        """
        return ("Weight", self.weight, self.expr._key())
