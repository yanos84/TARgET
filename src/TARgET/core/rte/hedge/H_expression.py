from abc import ABC, abstractmethod
from ...base.symbol import Symbol


class HorizontalExpression:
    """
    Factory for creating regular expressions over a set of symbols X.

    Represents the horizontal language algebra R(X).
    """

    def __init__(self, symbols):
        self.symbols = set(symbols)

    def atom(self, symbol):
        if symbol not in self.symbols:
            raise ValueError(
                f"Symbol {symbol} is not part of the horizontal alphabet"
            )
        return HAtom(symbol)

    def zero(self):
        return HZero()

    def one(self):
        return HOne()


class HExpression(ABC):
    """
    Base class for horizontal regular expressions.
    """

    def _key(self):
        pass

    def __eq__(self, value):
        return (
            isinstance(value, HExpression)
            and self._key() == value._key()
        )

    def __hash__(self):
        return hash(self._key())

    def __add__(self, other):
        """
        Horizontal union:

            r1 + r2
        """
        return HPlus(self, other)

    def __mul__(self, other):
        """
        Horizontal concatenation:

            r1.r2
        """
        return HConcat(self, other)

    def star(self):
        """
        Kleene star:

            r*
        """
        return HStar(self)

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)


class HZero(HExpression):
    """
    Empty language.
    """

    def __str__(self):
        return "0"

    def _key(self):
        return ("HZero",)


class HOne(HExpression):
    """
    Empty word epsilon.
    """

    def __str__(self):
        return "1"

    def _key(self):
        return ("HOne",)


class HAtom(HExpression):
    """
    A variable/symbol from X.
    """

    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def __str__(self):
        return str(self.symbol)

    def _key(self):
        return (
            "HAtom",
            self.symbol.name
        )


class HPlus(HExpression):
    """
    Union:

        r1 + r2
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left}+{self.right})"

    def _key(self):
        return (
            "HPlus",
            self.left._key(),
            self.right._key()
        )


class HConcat(HExpression):
    """
    Concatenation:

        r1.r2
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left}.{self.right})"

    def _key(self):
        return (
            "HConcat",
            self.left._key(),
            self.right._key()
        )


class HStar(HExpression):
    """
    Kleene star:

        r*
    """

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"({self.expr})*"

    def _key(self):
        return (
            "HStar",
            self.expr._key()
        )


# Example usage:
if __name__ == "__main__":

    x = Symbol("x")
    y = Symbol("y")
    z = Symbol("z")

    X = HorizontalExpression({x, y, z})

    hx = X.atom(x)
    hy = X.atom(y)
    hz = X.atom(z)


    # x+y
    r1 = hx + hy
    print(r1)

    # (x+y)*
    r2 = r1.star()
    print(r2)

    # (x+y)*.z
    r3 = r2 * hz
    print(r3)


    # Equality/hash test
    r4 = (X.atom(x) + X.atom(y)).star() * X.atom(z)

    print(r3 == r4)

    print(hash(r3))
    print(hash(r4))