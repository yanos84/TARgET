"""
********* This file contains the definition of the ranked rule (transition or transition function)***********

through this implementation, a transition (f,q_1,\ldots,q_n, q) (or f(q_1,_ldots, q_n)----> q)) is defined.
All the transition verifications are implemented here.  

"""

from .rule import Rule
from .state import State
from core.symbol import Ranked_Symbol
from typing import List

class ranked_Rule(Rule):
    """
    A class representing a ranked transition (rule).

    Attributes:
        func (ranked_Alpha): a ranked symbol instanciated from the ranked_Alpha class
        input(List[State]): the list of the input 
        output(State): the output state of the transition
    """
    def __init__(self, func:Ranked_Symbol =None, input_states : List[State] = None, output_state : State= None):

        """
        Initialize a transition rule

        Args:
        func (Ranked_Symbol): a ranked symbol instanciated from the Ranked_Symbol class
        input(List[State]): the list of the input 
        output(State): the output state of the transition    
        """
        super().__init__()
        self._func= func
        self._input: List[State] =input_states
        self._output:State = output_state

    
    """
    Defining setters and getters for the class attributes
    """
    @property
    def func(self):
        return self._func
    @func.setter
    def func(self,value):
        self._func = value
    @func.deleter
    def func(self):
        del _func

    @property
    def input_states(self):
        return self._input
    @input_states.setter
    def input_states(self,value: List[State]):
        self._input = value
    @property
    def output_state(self):
        return self._output
    @output_state.setter
    def output_state(self,value):
        self._output = value
    
    
    def is_valid(self)->bool:
        """
        Verify if the transition is valid by checking the adequation between the func rank and the number of input states
        
        Returns:
            bool: if the transition is valid or not
        """
        if self.func.rank == len(self.input_states):
            return True
        else:
            raise Exception ("The rank of the function is not equal to the states number in the rule")

    def get_rule_as_str(self):
        return self.func.name+"("+' '.join([i.name+"," for i in self.input_states ])[:-1]+")---->"+self.output_state.name


    
    def __str__(self):
        return self.get_rule_as_str()
    
    def __eq__(self, other):
        if not isinstance(other, ranked_Rule):
            return NotImplemented
        return (self.func == other.func and
                self.input_states == other.input_states and
                self.output_state == other.output_state )

    def __hash__(self):
        return hash((self.func, tuple(self.input_states), self.output_state))



#Example usage

if __name__ == '__main__':

    symb = Ranked_Symbol(name="f", rank=2)
    print(symb.name, symb.rank)
    s= State(name="q1", final=False, init=False)
    t=State(name="q2", final=False, init=False)
    u=State(name="q3", final=False, init=False)
    st = []
    st.append(s)
    st.append(t)
    print(st)
    rule = ranked_Rule(func = symb)
    rule.input_states = st
    rule.output_state = u
    print(rule)


