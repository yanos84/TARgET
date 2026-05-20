from abc import ABC, abstractmethod
from typing import List, Optional

class AbstractTree(ABC):
    """ Abstract base class for tree structures.
    This class defines the basic structure and operations for a tree, including adding children and checking well-formedness.
    Attributes:
    - symbol: The symbol associated with the node, which can be a string or a more complex object depending on the specific tree implementation.
    - children: A list of child nodes, which are also instances of AbstractTree.
    - parent: An optional reference to the parent node, allowing  for traversal up the tree.
    Methods:
    - __init__: Initializes the tree node with a given symbol and sets up the children and parent references.
    - add_child: Adds a child node to the current node, ensuring that the child is an instance of AbstractTree and properly sets the parent reference.
    - is_well_formed: An abstract method that must be implemented by subclasses to check if the tree structure adheres to specific constraints (e.g., ranked or unranked).
    - __str__: Provides a string representation of the tree, showing the symbol and its children in a readable format.
    - structure: Returns a tuple representation of the tree structure, which can be useful for comparisons and debugging.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol
        self._children: List["AbstractTree"] = []
        self._parent: Optional["AbstractTree"] = None

    @property
    def children(self) -> List["AbstractTree"]:
        return self._children

    @property
    def parent(self) -> Optional["AbstractTree"]:
        return self._parent

    def add_child(self, child: "AbstractTree"):
        if not isinstance(child, AbstractTree):
            raise TypeError("Child must be a tree")
        child._parent = self
        self._children.append(child)

    @abstractmethod
    def is_well_formed(self) -> bool:
        """Checks structural constraints (ranked/unranked)"""
        pass

    def __str__(self) -> str:
        if not self.children:
            return self.symbol
        return f"{self.symbol}({','.join(str(c) for c in self.children)})"
    
    def structure(self):
        return (
            self.symbol,
            tuple(child.structure() for child in self.children)
    )

    
