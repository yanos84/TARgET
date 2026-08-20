from TARgET.core.rte.rte import Rte, Zero, One, Plus, CProduct, CStar, function, Atom
from TARgET.core.base.symbol import Ranked_Symbol

"""
This module implements the nullable property for rational tree expressions (RTEs). The nullable property indicates whether a given RTE can generate the empty tree. The function `nullable` takes an RTE as input and returns a boolean value indicating whether the RTE is nullable or not. The implementation handles different types of RTEs, including Zero, One, Atom, function, Plus, CProduct, and CStar, by applying the appropriate logic to determine their nullability based on their structure and components. This functionality is essential for various operations on RTEs, such as simplification and normalization.    
"""


def nullable(r: Rte) -> bool:
    if isinstance(r, Zero):
        return False

    if isinstance(r, One):
        return True

    if isinstance(r, Atom):
        return False

    if isinstance(r, function):
        return False

    if isinstance(r, Plus):
        return any(nullable(t) for t in r.terms)

    if isinstance(r, CProduct):
        return nullable(r.left) and nullable(r.right)

    if isinstance(r, CStar):
        return True

    raise TypeError(f"Unsupported RTE type: {type(r)}")
    

# Example uage

if __name__ == "__main__":
    a = Ranked_Symbol("a")
    b = Ranked_Symbol("b")
    x = Ranked_Symbol("x")
    f = Ranked_Symbol("f", 2)
    g = Ranked_Symbol("g", 1)
    Ea = Atom(a)
    Eb = Atom(b)
    Ex = Atom(x)
    # trees
    fab = function(f, [Ea, Eb])
    gx  = function(g, [Ex])

    # rational tree expression
    rte = Plus(
        CStar(fab, b),
        CProduct(fab, gx, a)
    )

    print(rte)
    print(nullable(rte))