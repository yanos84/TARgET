from TARgET.rte.rte import Rte, Zero, One, Atom, function, CProduct, CStar, Plus
from TARgET.engine.rte.properties.semantics import accept_predicate
from TARgET.core.symbol import Symbol, Ranked_Symbol
from copy import deepcopy



class derivatives():
    """
    Compute the derivative of a rational tree expression.

    :param rte: The rational tree expression.
    :param symbol: The symbol with respect to which the derivative is computed.

    :returns: A set of rational tree expressions representing the derivative.
    :rtype: set[Rte]
    """


    def __init__(self):
        pass

    def derive(self, r: Rte, sym: Symbol)->set[Rte]:
        """
        Computes the derivative of a given rational tree expression (RTE) with respect to a specified symbol.
        :param r: The RTE for which the derivative is to be computed.
        :param sym: The symbol with respect to which the derivative is computed.
        :return: A set of resulting RTEs that represent the derivative of the original RTE with respect to the specified symbol.
        """
        response = set()
        if isinstance(r, (Zero, One, Atom)):
            return set()
        if isinstance(r, function):
            if sym == r.symbol:
                if not isinstance(sym, Ranked_Symbol):
                    comp = function(Symbol('ε'), r.args)
                else:
                    eps= Ranked_Symbol('ε', rank=r.symbol.rank)
                    _args = deepcopy(r.args)
                    comp = function(eps, _args)   
                return({comp})
            return set()
        
        if isinstance(r, Plus):
            for t in r.terms:
                response |= self.derive(t, sym)
            return response
        
        if isinstance(r, CStar):
            for d in self.derive(r.expr, sym):
                response.add(CProduct(d, r, r.concat))
            return response
        
        if isinstance(r, CProduct):
            if isinstance(sym, Ranked_Symbol):
                _concat=Ranked_Symbol(r.concat, rank=0)
            else:
                _concat =Symbol(r.concat)
            for d in self.derive(r.left, sym):
                response.add(CProduct(d, r.right, concat=_concat))
            if accept_predicate(r.left, r.concat):
                response |= (self.derive(r.right),sym)
            return(response)

#example usage

if __name__ == "__main__":
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
    #print(rte0)
    der = derivatives()
    #print(der.derive(rte0, f)) 
    #print(der.derive(rte0, g))           

# second example
    h = Ranked_Symbol("h", rank=1)
    E1 = function(f, [function(g,[function(h, [Atom(a)])]), function(g,[function(b, [])])])
    E1 = CStar(E1, a)
    #print(E1)
    E2= function(h, [function(a, [])]) 
    #print(E2)
    E3 = function(h,[function(b, [])])
    E2= Plus(E2,E3)
    #print(E2)
    rte1 = CProduct(E1, E2, b)
    print(rte1)
    print(der.derive(rte1, g))
              
