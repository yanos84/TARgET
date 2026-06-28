from abc import ABC, abstractmethod

class abs_minimize(ABC):
    """
    Abstract class for minimizing finite tree automata (FTAs).
    This class provides an interface for minimizing FTAs, which involves reducing the number of states and transitions while preserving the language accepted by the automaton. Subclasses must implement the `minimize`
    method, which performs the minimization process. Minimization is an important operation in automata theory, as it can lead to more efficient representations of automata and facilitate various operations such as equivalence checking and optimization.
    Attributes:
    - None
    Methods:
    - minimize: Abstract method to minimize the given FTA.
    """
    @abstractmethod
    def minimize(self, fta):
        pass
