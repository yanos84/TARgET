from .symbol import Ranked_Symbol
from .tree import AbstractTree

class RankedTree(AbstractTree):

    def __init__(self, symbol: Ranked_Symbol):
        super().__init__(symbol.name)
        self.ranked_symbol = symbol

    def add_child(self, child: "RankedTree"):
        if len(self.children) >= self.ranked_symbol.rank:
            raise ValueError(
                f"Symbol {self.symbol} has rank {self.ranked_symbol.rank}"
            )
        super().add_child(child)

    def is_well_formed(self) -> bool:
        if len(self.children) != self.ranked_symbol.rank:
            return False
        return all(child.is_well_formed() for child in self.children)


# Example usage
if __name__ == '__main__':
    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)

    root = RankedTree(symbol=f)
    child1 = RankedTree(symbol=a)
    child2 = RankedTree(symbol=a)

    root.add_child(child1)
    root.add_child(child2)

    print(root)  # Output: f(a,a)
    print("Is well formed:", root.is_well_formed())  # Output: True