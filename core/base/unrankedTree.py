
from .tree import AbstractTree


class UnrankedTree(AbstractTree):
    """
    A tree structure where each node can have an arbitrary number of children.
    This class extends AbstractTree and does not impose any constraints on the number of children a node can have. It provides methods to add children and check if the tree is well-formed, which in this case always returns True since there are no constraints on the number of children.
    """

    def is_well_formed(self) -> bool:
        return all(child.is_well_formed() for child in self.children)


# Example usage
if __name__ == '__main__':
    a = UnrankedTree(symbol="a")
    b = UnrankedTree(symbol="b")
    c = UnrankedTree(symbol="c")

    root = UnrankedTree(symbol="f")
    root.add_child(a)
    root.add_child(b)
    root.add_child(c)

    print(root)  # Output: f(a,b,c)
    print("Is well formed:", root.is_well_formed())  # Output: True