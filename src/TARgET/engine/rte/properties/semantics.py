from TARgET.core.rte.rte import Zero, One, function, Atom, CProduct, CStar, Rte, Plus
from . import nullable
from TARgET.core.base.symbol import Symbol, Ranked_Symbol

"""
This module implements the accept predicate for rational tree expressions (RTEs). The accept predicate is a function that determines whether a given RTE can accept a specific symbol. The function `accept_predicate` takes an RTE and a symbol as input and returns a boolean value indicating whether the RTE accepts the symbol. The implementation handles different types of RTEs, including Zero, One, Atom, function, Plus, CProduct, and CStar, by applying the appropriate logic to determine if the symbol can be accepted based on the structure and components of the RTE. This functionality is crucial for analyzing and manipulating RTEs in various applications, such as parsing and language recognition.    
"""


def accept_predicate(r: Rte, symb: Symbol)->bool:
    """
    Determines whether a given rational tree expression (RTE) accepts a specific symbol.
    """
    if isinstance(symb, Ranked_Symbol) and symb.rank!=0:
        raise ValueError("This function only tests leaf symbols (of rank 0)")
    if isinstance(r, (Zero, One)):
        return False
    if isinstance(r, Atom):
        if r.symbol==symb:
            return True
        else:
            return False
    if isinstance(r, function):
        if symb == r.symbol and len(r.args)==0:
            return True
        else:
            return False
    if isinstance(r, CProduct):
        return nullable(r.left) and accept_predicate(r.right)
    if isinstance(r, CStar):
        if r.concat == symb:
            return True
        else:
            return False
    if isinstance (r, Plus):
        _correct=False
        for t in r.terms:
            _correct = _correct or accept_predicate(t, symb)
        return _correct
        
# Example usage

if __name__=="__main__":
   # symbols
    a = Ranked_Symbol("a")
    b = Ranked_Symbol("b")
    f = Ranked_Symbol("f", rank=2)
    g = Ranked_Symbol("g", rank=1)

    # RTEs
    fab = CProduct(function(f, [function(a, []), function(b, [])]), function(f, [function(a, []), function(b, [])]), concat=a)
    gx = function(g, [function(a, [])])

    # rational tree expression
    rte0 = Plus(
        CStar(fab, concat=a),
        CProduct(fab, gx, concat=a),
        CStar(fab, concat=a)
    )
    print(rte0)
    print(accept_predicate(rte0, a))
