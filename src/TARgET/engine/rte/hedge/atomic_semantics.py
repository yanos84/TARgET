from TARgET.core.rte.rte import Plus, CProduct, CStar, Atom
from TARgET.core.rte.hedge.Hedge_Expression import HedgeFunction
from TARgET.core.rte.hedge.H_expression import (
    HExpression,
    HZero,
    HOne,
    HAtom,
    HPlus,
    HConcat,
    HStar
)


def accepts_single_symbol(expression):
    """
    Checks whether a hedge expression accepts a tree
    containing exactly one symbol.

    Examples of accepted trees:

        a

    and:

        f()

    where f() is represented as:

        f(1)

    Returns:
        True  -> expression accepts a leaf tree
        False -> otherwise
    """


    # Atomic symbol:
    #
    # a
    #
    # An atom is already a leaf tree.
    if isinstance(expression, Atom):
        return True


    # Unranked function:
    #
    # f(R(X))
    #
    # It accepts a leaf only if its horizontal language
    # accepts the empty word.
    if isinstance(expression, HedgeFunction):
        return horizontal_nullable(
            expression.horizontal
        )


    # Union:
    #
    # E1 + E2
    if isinstance(expression, Plus):
        return (
            accepts_single_symbol(expression.left)
            or
            accepts_single_symbol(expression.right)
        )


    # c-product:
    #
    # E1 .c E2
    #
    # A leaf can only be produced if the composition
    # does not introduce children.
    if isinstance(expression, CProduct):
        return (
            accepts_single_symbol(expression.left)
            and
            accepts_single_symbol(expression.right)
        )


    # c-star:
    #
    # E*c contains the neutral case.
    if isinstance(expression, CStar):
        return True


    raise TypeError(
        f"Unsupported hedge expression type: {type(expression)}"
    )



def horizontal_nullable(expression):
    """
    Checks whether a horizontal expression accepts epsilon.

    This corresponds to:

        ε ∈ L(R(X))
    """


    # Empty word:
    #
    # 1
    if isinstance(expression, HOne):
        return True


    # Empty language:
    #
    # 0
    if isinstance(expression, HZero):
        return False


    # Variable:
    #
    # x
    #
    # A variable represents a child hedge,
    # so it cannot disappear.
    if isinstance(expression, HAtom):
        return False


    # Union:
    #
    # R1 + R2
    if isinstance(expression, HPlus):
        return (
            horizontal_nullable(expression.left)
            or
            horizontal_nullable(expression.right)
        )


    # Concatenation:
    #
    # R1.R2
    if isinstance(expression, HConcat):
        return (
            horizontal_nullable(expression.left)
            and
            horizontal_nullable(expression.right)
        )


    # Star:
    #
    # R*
    #
    # Always accepts epsilon.
    if isinstance(expression, HStar):
        return True


    raise TypeError(
        f"Unsupported horizontal expression type: {type(expression)}"
    )

#Example of use from TARgET.core.rte.hedge
if __name__ == "__main__":
    from TARgET.core.base.symbol import Symbol

    from TARgET.core.rte.hedge.H_expression import HorizontalExpression
    from TARgET.core.rte.hedge.Hedge_Expression import HedgeFunction

    from TARgET.core.rte.rte import Atom




    a = Symbol("a")
    f = Symbol("f")

    x = Symbol("x")


    # Atomic tree:
    #
    # a
    A = Atom(a)

    print(A)
    print(
        accepts_single_symbol(A)
    )


    # Function leaf:
    #
    # f()
    #
    # represented as f(1)

    X = HorizontalExpression({x})

    F = HedgeFunction(
        f,
        X.one()
    )

    print(F)
    print(
        accepts_single_symbol(F)
    )


    # Function with children:
    #
    # f(x)

    FX = HedgeFunction(
        f,
        X.atom(x)
    )

    print(FX)
    print(
        accepts_single_symbol(FX)
    )