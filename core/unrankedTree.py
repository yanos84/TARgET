
from .tree import AbstractTree


class UnrankedTree(AbstractTree):

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