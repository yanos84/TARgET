from abc import ABC, abstractmethod
from fta.abst_fta import Fta


class FtaGenerator(ABC):
    """
    Abstract base class for all FTA generators.
    """

    @abstractmethod
    def generate(self) -> Fta:
        """
        Generate and return an FTA.
        """
        pass
