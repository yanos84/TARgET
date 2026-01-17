from rte.rte import Rte, Zero, One, Plus, CProduct, CStar, function, Atom
from core.symbol import Ranked_Symbol


def nullable(r: Rte)->bool:
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