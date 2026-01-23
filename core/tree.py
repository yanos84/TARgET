from abc import ABC, abstractmethod
from typing import List, Optional

class AbstractTree(ABC):

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

    
