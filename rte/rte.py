"""*********************This is the abstract class RTE from which all rte variantes herit.

The rational expressions are presented in their formal form. Classes like [A Z], digit ..ect are not supported.
Only the oparators +,*c, .c for trees or +, *, . for strings are taken into account.
"""

from abc import ABC, abstractmethod
from TARgET.core.symbol import Symbol, Ranked_Symbol

class Rte(ABC):
    """
		Abstract base class for Rational Tree Expressions (RTE).
		Defines the interface for all RTE variants.
	"""

    def _key(self):
        """
            Provides a unique key for the RTE instance.
            Used for hashing and equality checks.
        """
        pass

    def __eq__(self, value):
        """
        Checks equality between two RTE instances based on their keys."""
        return isinstance(value, Rte) and self._key() == value._key()
    
    def __hash__(self):
        """
        Returns a hash value for the RTE instance based on its key."""
        return hash(self._key())

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return str(self)
		

class Zero(Rte):
    """
		Represents the zero element in Rational Tree Expressions (RTE).	
	"""	
    def __str__(self):
        return "0"
    
    def _key(self):
        return ("Zero",)

class One(Rte):
    """
		Represents the one element in Rational Tree Expressions (RTE).
	"""
    def __str__(self):
        return "1"

    def _key(self):
        return ("One",)
    
class Atom(Rte):
    """
        Represents an atomic RTE, which is simply a symbol.
    """
    def __init__(self, symbol: Symbol):
        if isinstance(symbol, Ranked_Symbol) and symbol.rank != 0:
            raise ValueError("Atom symbol must be a leaf ranked Symbol (rank 0)")
        self.symbol = symbol

    def __str__(self):
        return str(self.symbol)
    
    def _key(self):
        return ("Atom", self.symbol.name)


class function(Rte):
    """
		Represents an application of a symbol f to RTEs (E1,...En) -> f(E1,...,En).    
	"""
    def __init__(self, symbol: Symbol, args: list[Rte] | None = None):
        """
        Initializes a Tree_node with a symbol and its arguments.
        :param symbol: The symbol representing the function or constructor.
        :param args: A list of RTEs representing the arguments to the symbol.
        """
        self.symbol = symbol
        self.args = args

        if isinstance(symbol, Ranked_Symbol): # check if the RTE is well formed according to the rank of the symbol
            if self.args is None:
                self.args = []
            if len(self.args) != symbol.rank and symbol.rank != 0:
                raise ValueError(
                    f"Symbol {symbol.name} has rank {symbol.rank}, "
                    f"but got {len(self.args)} arguments"
                )



    def __str__(self):
        if self.args is None or len(self.args) == 0:
            return str(self.symbol)
        return f"{self.symbol}(" + ",".join(str(a) for a in self.args) + ")"
    
    def _key(self):
        return (
            "function",
            self.symbol.name,
            tuple(arg._key() for arg in self.args)
        )

class Plus(Rte):
    """
        Represents the sum of multiple RTEs (E1 + E2 + ... + En).
    """
    def __init__(self, *terms):
        flat = []
        for t in terms:
            if isinstance(t, Plus):
                flat.extend(t.terms)
            else:
                flat.append(t)
        # remove duplicates using equality
        unique = set(flat)

        # sort canonically
        self.terms = tuple(sorted(unique, key=lambda x: x._key())) # save 


    def __str__(self):
        return " + ".join(str(t) for t in self.terms)
    
    def _key(self):
        return ("Plus", tuple(t._key() for t in self.terms))
    
class CProduct(Rte):
    def __init__(self, left: Rte, right: Rte, concat: Symbol):
        """
        Initializes a CProduct with left and right operands and a concatenation operator.
        :param left: The left RTE operand.
        :param right: The right RTE operand.
        :param concat: The concatenation operator (must be a Symbol).
        """


        if not isinstance(concat, Symbol):
            raise ValueError("Concatenation operator must be a Symbol")
        if isinstance(concat, Ranked_Symbol) and concat.rank != 0:
            raise ValueError("Concatenation operator must be a leaf ranked Symbol (rank 0)")
        
        self.left = left
        self.right = right
        self.concat = concat.name

    def __str__(self):
        return f"({self.left}).{self.concat}({self.right})"
    
    def _key(self):
        return (
            "CProduct",
            self.concat,
            self.left._key(),
            self.right._key()
        )

class CStar(Rte):
    """
        Represents the Kleene star operation on an RTE (E*), with a concatenation operator.
    """
    def __init__(self, expr: Rte, concat : Symbol):
        if not isinstance(concat, Symbol):
            raise ValueError("Concatenation operator must be a Symbol")
        if isinstance(concat, Ranked_Symbol) and concat.rank != 0:
            raise ValueError("Concatenation operator must be a leaf ranked Symbol (rank 0)")
        self.expr = expr
        self.concat = concat

    def __str__(self):
        return f"({self.expr})*{self.concat}"
    
    def _key(self):
        return (
            "CStar",
            self.concat.name,
            self.expr._key()
        )

# Example usage
if __name__ == "__main__":
# symbols
    a, b, x, f, g = Ranked_Symbol("a"), Ranked_Symbol("b"), Ranked_Symbol("x"), Ranked_Symbol("f", 2), Ranked_Symbol("g", 1)
    Ea, Eb, Ex = Atom(a), Atom(b), Atom(x)
    # trees
    fab = function(f, [Ea, Eb])
    gx  = function(g, [Ex])
    # rational tree expression
    rte = Plus(
        CStar(fab, b),
        CProduct(fab, gx, a)
    )
    print(rte)

