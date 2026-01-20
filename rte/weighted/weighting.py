from abc import ABC, abstractmethod
from algebric.semiring import Semiring
from rte.rte import Rte, Zero, One, Atom, function, Plus, CProduct, CStar
from rte.weighted.weight import Weight

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

class SemiringRteWeighting(RteWeighting):
    def __init__(self, semiring_cls):
        self.S = semiring_cls

    def weight(self, rte: Rte) -> Semiring:

        if isinstance(rte, Zero):
            return self.S.zero()

        if isinstance(rte, One):
            return self.S.one()

        if isinstance(rte, Atom):
            return self.S.one()      # neutral symbol

        if isinstance(rte, function):
            return self.S.one()      # symbol itself has no weight

        if isinstance(rte, Plus):
            return sum(
                (self.weight(t) for t in rte.terms),
                self.S.zero()
            )

        if isinstance(rte, CProduct):
            return self.weight(rte.left) * self.weight(rte.right)

        if isinstance(rte, CStar):
            # semiring star or Kleene closure
            return self.weight(rte.expr).star()

        if isinstance(rte, Weight):
            return rte.weight * self.weight(rte.expr)

        raise TypeError(type(rte))

#example usage

if __name__ == "__main__":
    from algebric.trop_semiring import TropicalSemiring as TS
    from core.symbol import Ranked_Symbol
    from rte.weighted.weight_rte_print import WeightedRtePrinter as WRP
    f= Ranked_Symbol('f', rank = 2)
    a = Ranked_Symbol('a')
    b= Ranked_Symbol('b')
    E = Weight(TS(1.0), Weight(TS(2.0),Plus(function(f, [Atom(a), Atom(b)]), function(f, [Atom(b), Atom(a)]))))
    print("The weighted expression", E)
    W = SemiringRteWeighting(TS)
    print("The total weight is" , W.weight(E))   # 𝕋(3.0)
