from abc import ABC, abstractmethod
from TARgET.core.fta.abst_fta import Fta

class Abs_prod(ABC):
    """
    Abstract class for computing the product of two finite tree automata (FTAs).
    This class provides an interface for computing the product of two FTAs, which involves combining their states and transitions to create a new FTA that accepts the intersection of the languages accepted by the original FTAs. Subclasses must implement the `product` method, which performs the product computation. The"" product operation is essential for various operations in automata theory, such as language intersection and equivalence checking.
    Attributes:
    - None
    Methods:
    - product: Abstract method to compute the product of two FTAs.
    """
    @abstractmethod
    def product(self, fta1: Fta, fta2: Fta) -> Fta:
        """Compute the product of two finite tree automata."""
        pass