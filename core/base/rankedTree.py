from .symbol import Ranked_Symbol
from .tree import AbstractTree

class RankedTree(AbstractTree):
    """ A tree structure where each node is associated with a ranked symbol.
     The number of children of each node must match the rank of its symbol.
      This class extends AbstractTree and adds constraints based on the rank of the symbols.
         It provides methods to add children while ensuring the tree remains well-formed according to the ranked symbols.
      Attributes:
      - ranked_symbol: The Ranked_Symbol associated with the node, which determines the number of children it can have.
      Methods:
      - __init__: Initializes the RankedTree with a given Ranked_Symbol.
      - add_child: Adds a child to the tree, ensuring it does not exceed the rank of the symbol.
      - is_well_formed: Checks if the tree is well-formed according to the ranked symbol's rank, ensuring that each node has the correct number of children.    
       
     """

    def __init__(self, symbol: Ranked_Symbol):
        super().__init__(symbol.name)
        self.ranked_symbol = symbol

    def add_child(self, child: "RankedTree"):
        """ Add a child to the tree, ensuring it does not exceed the rank of the symbol. """
        if len(self.children) >= self.ranked_symbol.rank:
            raise ValueError(
                f"Symbol {self.symbol} has rank {self.ranked_symbol.rank}"
            )
        super().add_child(child)

    def is_well_formed(self) -> bool:
        """Check if the tree is well-formed according to the ranked symbol's rank. """
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