"""*********************This is the abstract class RTE from which all rte variantes herit.

The rational expressions are presented in their formal form. Classes like [A Z], digit ..ect are not supported.
Only the oparators +,*c, .c for trees or +, *, . for strings are taken into account.
"""

from abc import ABC, abstractmethod
from core.symbol import Symbol, Ranked_Symbol

class Rte(ABC):
    '''
	Docstring for Rte class
		Abstract base class for Rational Tree Expressions (RTE).
		Defines the interface for all RTE variants.
	'''
    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)
		

class Zero(Rte):
    '''
	Docstring for Zero class
		Represents the zero element in Rational Tree Expressions (RTE).	
	'''	
    def __str__(self):
        return "0"

class One(Rte):
    '''
	Docstring for One class
		Represents the one element in Rational Tree Expressions (RTE).
	'''
    def __str__(self):
        return "1"




class Arity(Rte):
    '''
	Docstring for Arity
		Represents an application of a symbol f to RTEs (E1,...En) -> f(E1,...,En).
	'''
    def __init__(self, symbol: Symbol, args: list[Rte]=[]):
        assert len(args) == symbol.arity
        self.symbol = symbol
        self.args = args

    def __str__(self):
        if self.symbol.arity == 0:
            return str(self.symbol)
        return f"{self.symbol}(" + ",".join(str(a) for a in self.args) + ")"

class Plus(Rte):
    def __init__(self, *terms):
        self.terms = terms

    def __str__(self):
        return " + ".join(str(t) for t in self.terms)
    
class CProduct(Rte):
    def __init__(self, left: Rte, right: Rte):
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left}).c({self.right})"

class CStar(Rte):
    def __init__(self, expr: Rte):
        self.expr = expr

    def __str__(self):
        return f"({self.expr})*c"

# Example usage
if __name__ == "__main__":
# symbols
    a = Ranked_Symbol("a")
    b = Ranked_Symbol("b")
    x = Ranked_Symbol("x")
    f = Ranked_Symbol("f", 2)
    g = Ranked_Symbol("g", 1)
    # trees
    fab = Arity(f, [Arity(a), Arity(b)])
    gx  = Arity(g, [Arity(x)])

    # rational tree expression
    rte = Plus(
        CStar(fab),
        CProduct(fab, gx)
    )

    print(rte)

