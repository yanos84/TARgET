# core/symbol.py

class Symbol:
    """Represents a basic symbol with a name.
    This class serves as a base for more complex symbol types, such as ranked symbols.
    Attributes:
        - name: The name of the symbol, which is used for identification and comparison.
    Methods:
        - __init__: Initializes the symbol with a given name.
        - __str__: Returns the string representation of the symbol, which is its name.
        - __eq__: Compares two symbols for equality based on their names.
        - __hash__: Provides a hash value for the symbol, allowing it to be used in sets and as dictionary keys.
    """
    
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name
    
    def __eq__(self, symb):
        return isinstance(symb, Symbol) and self.name == symb.name
    
    def __hash__(self):
        return hash(self.name)


class Ranked_Symbol(Symbol):
    """Represents a ranked symbol with fixed rank."""

    def __init__(self, name: str, rank: int = 0):
        super().__init__(name)
        self.rank = rank

    def __eq__(self, symb):
        return (
            isinstance(symb, Ranked_Symbol) and
            self.name == symb.name and
            self.rank == symb.rank
        )

    def __hash__(self):
        # Must match equality
        return hash((self.name, self.rank))

    def __str__(self):
        return self.name
