from abc import ABC, abstractmethod
from TARgET.core.fta.abst_fta import Fta

class AbsEmptiness(ABC):
    """
    Abstract class for checking the emptiness of finite tree automata (FTAs).
    This class provides an interface for determining whether a given FTA accepts any trees. Subclasses must implement the `is_empty` method, which checks if the structure is empty. The emptiness check is crucial for various operations in automata theory, such as determining equivalence or performing set operations on FTAs.
    Attributes:
        - None
    Methods:
        - is_empty: Abstract method to check if the structure is empty.
    """
    @abstractmethod
    def is_empty(self, fta: Fta) -> bool:
        """Check if the structure is empty."""
        pass