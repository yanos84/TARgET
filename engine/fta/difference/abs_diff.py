from abc import ABC, abstractmethod
from fta.abst_fta import Fta
from engine.fta.emptiness.abs_emptiness import AbsEmptiness

class Abs_Diff(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def diff(self, fta1:Fta, fta2:Fta) -> Fta:
        pass

    def is_equivalent(self, fta1:Fta, fta2:Fta) -> bool:
        difference_fta = self.diff(fta1, fta2)
        emptiness_checker = AbsEmptiness()
        return emptiness_checker.is_empty(difference_fta)