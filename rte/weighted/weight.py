from rte.rte import Rte
from algebric.semiring import Semiring

class Weight(Rte):
    """
    Represents k ⊗ E
    """
    def __init__(self, weight: Semiring, expr: Rte):
        self.weight = weight
        self.expr = expr

    def __str__(self):
        return f"{self.weight} ⊗ ({self.expr})"

    def _key(self):
        return ("Weight", self.weight, self.expr._key())
