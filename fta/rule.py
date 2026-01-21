#********The abstract class defining rules (transition functions)**************
# The user can inherit from this class in order to define more sophisticated transition rules such as transducers ...

from abc import ABC, abstractmethod
from .state import State
from core.symbol import Symbol
from typing import List
from algebric.semiring import Semiring

class Rule(ABC):
    @abstractmethod
    def __init__(self, symbol:Symbol =None, input_states : List[State] = None, output_state : State= None, is_weighted : bool = False, weight:Semiring = None):
        pass
