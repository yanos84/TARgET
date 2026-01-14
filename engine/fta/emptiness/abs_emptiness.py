from abc import ABC, abstractmethod
from fta.abst_fta import Fta

class AbsEmptiness(ABC):
    @abstractmethod
    def is_empty(self, fta: Fta) -> bool:
        """Check if the structure is empty."""
        pass