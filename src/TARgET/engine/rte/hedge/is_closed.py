from TARgET.core.rte.hedge.Hedge_Expression import HedgeExpression, HedgeFunction
from TARgET.core.rte.hedge.H_expression import HExpression, HAtom, HPlus, HConcat, HStar, HZero, HOne
from TARgET.core.rte.rte import CProduct, Plus, CStar


def is_closed(expression):
    """
    Checks whether a hedge expression contains no remaining variables.

    A hedge expression is closed if every horizontal language R(X)
    appearing in f(R(X)) is variable-free.
    """

    if isinstance(expression, HedgeFunction):
        return horizontal_is_closed(expression.horizontal)


    # Operators inherited from Rte
    elif isinstance(expression, Plus):
        return (
            is_closed(expression.left)
            and is_closed(expression.right)
        )


    elif isinstance(expression, CProduct):
        return (
            is_closed(expression.left)
            and is_closed(expression.right)
        )


    elif isinstance(expression, CStar):
        return is_closed(expression.expr)


    else:
        raise TypeError(
            f"Unsupported hedge expression type: {type(expression)}"
        )



def horizontal_is_closed(expression):
    """
    Checks whether a horizontal expression contains variables.
    """

    if isinstance(expression, HAtom):
        # A horizontal atom represents a variable X
        return False


    elif isinstance(expression, (HZero, HOne)):
        return True


    elif isinstance(expression, (HPlus, HConcat)):
        return (
            horizontal_is_closed(expression.left)
            and horizontal_is_closed(expression.right)
        )


    elif isinstance(expression, HStar):
        return horizontal_is_closed(expression.expr)


    else:
        raise TypeError(
            f"Unsupported horizontal expression type: {type(expression)}"
        )


#Example usage:
if __name__ == "__main__":
    from TARgET.core.rte.hedge.H_expression import HorizontalExpression
    from TARgET.core.rte.hedge.Hedge_Expression import HedgeFunction
    from TARgET.core.rte.rte import CProduct
    from TARgET.core.base.symbol import Symbol


    x = Symbol("x")
    y = Symbol("y")

    X = HorizontalExpression({x, y})

    hx = X.atom(x)
    hy = X.atom(y)

    R = hx + hy.star()


    F = HedgeFunction(
            Symbol("f"),
            R
        )


    print(F)

    print(is_closed(F))