from abc import ABC, abstractmethod

class Acceptor(ABC):
    """
    Generic interface for tree acceptance algorithms.
    """

    @abstractmethod
    def accepts(self, automaton, tree) -> bool:
        """
        Check whether the automaton accepts the given tree.

        :param automaton: The tree automaton.
        :param tree: The input tree structure.

        :returns: ``True`` if the automaton accepts the tree; otherwise, ``False``.
        :rtype: bool
        """
        pass
