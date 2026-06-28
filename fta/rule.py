#********The abstract class defining rules (transition functions)**************
# The user can inherit from this class in order to define more sophisticated transition rules such as transducers ...

from abc import ABC, abstractmethod
from .state import State
from TARgET.core.symbol import Symbol
from typing import List
from TARgET.algebric.semiring import Semiring

class Rule(ABC):
    """
    An abstract class defining transition rules for finite tree automata. All transition rules inherit directly or indirectly from Rule.   
    """
    @abstractmethod
    def __init__(self, func:Symbol =None, input_states : List[State] = None, output_state : State= None, is_weighted : bool = False, weight:Semiring = None):
        self.func = func
        self.input_states = input_states
        self.output_state = output_state
        self.is_weighted = is_weighted
        self.weight = weight
        if not self.is_weighted and weight!=None:
            raise ValueError("The rule is unweighted but you add a weight to it")
