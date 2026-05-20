from abc import ABC, abstractmethod
from fta.abst_fta import Fta
from engine.fta.emptiness.abs_emptiness import AbsEmptiness

class Abs_Diff(ABC):
    """Class to compute the difference between two finite tree automata (FTAs).
    The difference of two FTAs, FTA1 and FTA2, is a new FTA that accepts exactly the trees that are accepted by FTA1 but not by FTA2. This is achieved by constructing a new FTA that combines the states and transitions of both FTAs while ensuring that the acceptance conditions reflect the difference. The resulting difference FTA can be used to check 
    for non-acceptance of trees in FTA2 that are accepted by FTA1, or to perform operations like intersection and union with other FTAs.
    Attributes:
    - None"""
    def __init__(self):
        pass
    @abstractmethod
    def diff(self, fta1:Fta, fta2:Fta) -> Fta:
        pass

    def is_equivalent(self, fta1:Fta, fta2:Fta) -> bool:
        difference_fta = self.diff(fta1, fta2)
        emptiness_checker = AbsEmptiness()
        return emptiness_checker.is_empty(difference_fta)