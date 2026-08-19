from TARgET.core.rte.rte import Plus, CProduct, CStar, Atom
from TARgET.core.rte.hedge.Hedge_Expression import HedgeFunction
from TARgET.core.rte.hedge.H_expression import (
    HZero,
    HOne,
    HAtom,
    HPlus,
    HConcat,
    HStar
)


def singleton(expression, a):
    """
    Checks whether the single-symbol tree a belongs to the
    semantics of the hedge expression.

    That is, this procedure decides whether:

        a ∈ [[expression]]

    where a is a specific symbol in the alphabet.

    Returns:
        True  -> the single-symbol tree a is accepted
        False -> otherwise
    """

    # Atomic expression:
    #
    # b
    #
    # The expression accepts exactly the single-symbol tree b.
    if isinstance(expression, Atom):
        return expression.symbol == a


    # Hedge function:
    #
    # b(R)
    #
    # This represents the single-symbol tree b exactly when
    # the horizontal expression R accepts the empty hedge.
    if isinstance(expression, HedgeFunction):
        return (
            expression.symbol == a
            and
            horizontal_nullable(expression.horizontal)
        )


    # Union:
    #
    # E1 + E2
    #
    # A single-symbol tree is accepted if it is accepted
    # by either operand.
    if isinstance(expression, Plus):
        return (
            singleton(expression.left, a)
            or
            singleton(expression.right, a)
        )


    # c-product:
    #
    # E1 .c E2
    #
    # If a = c, both expressions must accept the singleton a.
    #
    # If a != c, the singleton a can either already be produced
    # by E1, or it can be produced by E2 when E1 produces c.
    if isinstance(expression, CProduct):
        c = expression.symbol

        if a == c:
            return (
                singleton(expression.left, a)
                and
                singleton(expression.right, a)
            )

        return (
            singleton(expression.left, a)
            or
            (
                singleton(expression.left, c)
                and
                singleton(expression.right, a)
            )
        )


    # c-star:
    #
    # E*c
    #
    # For singleton membership, the closure does not introduce
    # a new singleton symbol. Therefore, a is accepted exactly
    # when it is accepted by E.
    if isinstance(expression, CStar):
        return singleton(expression.expression, a)


    raise TypeError(
        f"Unsupported hedge expression type: {type(expression)}"
    )



def horizontal_nullable(expression):
    """
    Checks whether a horizontal expression accepts epsilon.

    That is:

        ε ∈ [[expression]]
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
    # A variable represents a non-empty child hedge.
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
    # R1 . R2
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


# Example
if __name__ == "__main__":
    from TARgET.core.base.symbol import Symbol
    from TARgET.core.rte.hedge.H_expression import HorizontalExpression

    a = Symbol("a")
    f = Symbol("f")
    x = Symbol("x")


    # Atomic tree:
    #
    # a
    A = Atom(a)

    print(A)
    print(singleton(A, a))   # True
    print(singleton(A, f))   # False


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
    print(singleton(F, f))   # True
    print(singleton(F, a))   # False


    # Function with children:
    #
    # f(x)
    FX = HedgeFunction(
        f,
        X.atom(x)
    )

    print(FX)
    print(singleton(FX, f))  # False