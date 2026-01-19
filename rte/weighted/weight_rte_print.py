from rte.rte import Rte, Zero, One, Atom, function, CStar, CProduct, Plus
from algebric.semiring import Semiring

class WeightedRtePrinter:
    def __init__(self, weights: dict[str, Semiring]):
        self.weights = weights
    
    def print(self, rte: Rte, global_weight = None) -> str:
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


