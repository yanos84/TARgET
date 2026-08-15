from abc import ABC, abstractmethod
from ...base.symbol import Symbol


class HedgeExpression(ABC):
    """
    Abstract base class for hedge expressions.

    Hedge expressions represent unranked trees:

        HE ::= f(R(X))
             | HE + HE
             | HE .c HE
             | HE*c
    """

    def _key(self):
        """
        Unique representation used for equality and hashing.
        """
        pass


    def __eq__(self, value):
        return (
            isinstance(value, HedgeExpression)
            and self._key() == value._key()
        )


    def __hash__(self):
        return hash(self._key())


    @abstractmethod
    def __str__(self):
        pass


    def __repr__(self):
        return str(self)



class HedgeFunction(HedgeExpression):
    """
    Represents an unranked hedge constructor:

        f(R(X))

    where:
        - f is an unranked symbol
        - R(X) is a horizontal regular expression
    """

    def __init__(self, symbol: Symbol, horizontal):
        self.symbol = symbol
        self.horizontal = horizontal


    def __str__(self):
        return f"{self.symbol}({self.horizontal})"


    def _key(self):
        return (
            "HedgeFunction",
            self.symbol.name,
            self.horizontal._key()
        )


    # Example usage:
if __name__ == "__main__":
    from .H_expression import HorizontalExpression
    from ..rte import CProduct, Plus, CStar
    x = Symbol("x")
    y = Symbol("y")

    f = Symbol("f")
    g = Symbol("g")
    X = HorizontalExpression({x, y})

    hx = X.atom(x)
    hy = X.atom(y)
    R1 = hx + hy.star()
    R2 = hy.star()
    F = HedgeFunction(
        f,
        R1
    )
    G = HedgeFunction(
        g,
        R2
    )



    # f(x+y*) + g(y*)
    expr1 = Plus(F, G)

    print(expr1)


    # f(x+y*) ._x g(y*)
    expr2 = CProduct(
                F,
                G,
                x
            )

    print(expr2)

    H = Plus(
        CProduct(
            F,
            G,
            x
        ),
        HedgeFunction(
            f,
            R2
        )
    )


    print(H)