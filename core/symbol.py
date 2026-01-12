# core/symbol.py

class Symbol:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)


class Ranked_Symbol(Symbol):
    """Represents a ranked symbol with fixed rank."""

    def __init__(self, name: str, rank: int = 0):
        super().__init__(name)
        self.rank = rank

    def __str__(self):
        return self.name
