from abc import ABC, abstractmethod

class Acceptor(ABC):
    """
    Generic interface for tree acceptance algorithms.
    """

    @abstractmethod
    def accepts(self, automaton, tree) -> bool:
        """
        Check whether the automaton accepts the given tree.

        Args:
            automaton: a tree automaton
            tree: a tree structure

        Returns:
            bool
        """
        pass
