from abc import ABC, abstractmethod
from algebric.semiring import Semiring
from rte.rte import Rte, Zero, One, Atom, function, Plus, CProduct, CStar

class RteWeighting(ABC):
    """
    Interface for weighted semantics (power series).
    Interprets an RTE as a semiring value.
    """

    @abstractmethod
    def weight(self, rte: Rte) -> Semiring:
        pass


class SemiringRteWeighting(RteWeighting):
    """
    Generic weighting of RTEs over a given semiring.
    """

    def __init__(self, semiring_cls: type[Semiring]):
        self.S = semiring_cls

    def weight(self, rte: Rte) -> Semiring:

        if isinstance(rte, Zero):
            return self.S.zero()

        if isinstance(rte, One):
            return self.S.one()

        if isinstance(rte, Atom):
            # default: atoms have weight 1
            return self.S.one()

        if isinstance(rte, function):
            # weight of f(E1,...,En) = ⊗ weight(Ei)
            w = self.S.one()
            for arg in rte.args:
                w = w * self.weight(arg)
            return w

        if isinstance(rte, Plus):
            w = self.S.zero()
            for t in rte.terms:
                w = w + self.weight(t)
            return w

        if isinstance(rte, CProduct):
            return self.weight(rte.left) * self.weight(rte.right)

        if isinstance(rte, CStar):
            # Kleene star: 1 ⊕ x ⊕ x² ⊕ ...
            # For now, assume star = 1 (valid for tropical / boolean)
            return self.S.one()

        raise TypeError(f"Unsupported RTE type: {type(rte)}")

class SymbolWeightedRteWeighting(SemiringRteWeighting):
    """
    Weighted semantics compatible with weighted tree automata:
    each symbol application contributes a weight.
    """

    def __init__(self, semiring_cls, symbol_weights: dict[str, Semiring]):
        super().__init__(semiring_cls)
        self.symbol_weights = symbol_weights

    def symbol_weight(self, symbol_name: str) -> Semiring:
        return self.symbol_weights.get(symbol_name, self.S.one())

    def weight(self, rte: Rte) -> Semiring:
        if isinstance(rte, Zero):
            return self.S.zero()

        if isinstance(rte, One):
            return self.S.one()

        if isinstance(rte, Atom):
            # nullary symbol application
            return self.symbol_weight(rte.symbol.name)

        if isinstance(rte, function):
            # f(E1,...,En) → w(f) ⊗ Π w(Ei)
            w = self.symbol_weight(rte.symbol.name)
            for arg in rte.args:
                w = w * self.weight(arg)
            return w

        if isinstance(rte, Plus):
            w = self.S.zero()
            for t in rte.terms:
                w = w + self.weight(t)
            return w

        if isinstance(rte, CProduct):
            return self.weight(rte.left) * self.weight(rte.right)

        if isinstance(rte, CStar):
            # standard assumption: star = 1
            return self.S.one()

        raise TypeError(f"Unsupported RTE type: {type(rte)}")

#example usage

if __name__ == "__main__":
    from algebric.trop_semiring import TropicalSemiring
    from core.symbol import Ranked_Symbol
    from rte.weighted.weight_rte_print import WeightedRtePrinter as WRP
    f= Ranked_Symbol('f', rank = 2)
    a = Ranked_Symbol('a')
    b= Ranked_Symbol('b')
    E = Plus(function(f, [Atom(a), Atom(b)]), function(f, [Atom(b), Atom(a)]))
    print(E)
    weights = {
    "a": TropicalSemiring(1.0),
    "b": TropicalSemiring(2.0),
    "f": TropicalSemiring(4.0)
}
    W = SymbolWeightedRteWeighting(TropicalSemiring, weights)
    print(W.weight(E))   # 𝕋(3.0)
    printer = WRP(weights)
    print(printer.print(E, W.weight(E)))