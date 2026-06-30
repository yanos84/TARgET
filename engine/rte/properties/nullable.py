from TARgET.rte.rte import Rte, Zero, One, Plus, CProduct, CStar, function, Atom
from TARgET.core.symbol import Ranked_Symbol

"""
This module implements the nullable property for rational tree expressions (RTEs). The nullable property indicates whether a given RTE can generate the empty tree. The function `nullable` takes an RTE as input and returns a boolean value indicating whether the RTE is nullable or not. The implementation handles different types of RTEs, including Zero, One, Atom, function, Plus, CProduct, and CStar, by applying the appropriate logic to determine their nullability based on their structure and components. This functionality is essential for various operations on RTEs, such as simplification and normalization.    
"""


def nullable(r: Rte)->bool:
    """
    Determines whether a given rational tree expression (RTE) is nullable, meaning it can generate the empty tree.
    """
    if isinstance(r, (Zero, Atom, function)):
        return False
    if isinstance(r, (One, CStar)):
        return True
    if isinstance(r, Plus):
        return any(nullable(t) for t in r.terms)
    if isinstance(r, CProduct):
        return nullable(r.left) and nullable(r.right)
    raise ValueError("Unknown Rte type")
    

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