from abc import ABC, abstractmethod
from fta.abst_fta import Fta

class Abs_prod(ABC):
    @abstractmethod
    def product(self, fta1: Fta, fta2: Fta) -> Fta:
        """Compute the product of two finite tree automata."""
        pass