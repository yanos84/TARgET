"""
************************Non deterministic union of two fta *********************************

Implementation of a straithforward union algorithm that simply unifies alphabets, stats and transitions into a non deterministic
union fta
"""

from typing import List

import sys
sys.path.append('../TARgET/fta')

from fta import Fta
from state import State
from alphabet import ranked_Alpha
from rankedRule import ranked_Rule
from rankedfta import ranked_Fta
import copy

class Union():
    """
    Union class: it takes two fta A1 and A2 to be unified in a nondeterministic new fta. 

    Attributes:
        _A1: refers to the first automaton
        _A2: refers to the second automaton
        union_Fta: The union fta
    """
    def __init__(self, A1, A2):
        self._A1: ranked_Fta= A1
        self._A2 : ranked_Fta = A2
        self.union_Fta : ranked_Fta = ranked_Fta(alphabet = [], fta_states = [], transitions = [])

    def nondeterministic_union(self):
        self.union_Fta.name = "Union "+self._A1.name+"_"+self._A2.name
        #self.union_Fta.
        """
        Unifies two fta. It simply applies union on alphabet, transitions and states sets.
        """
        self.union_Fta.extend_States_list(self._A1.states_list)
        _temp:List[State] = []
        for i in self._A2.states_list:
            j = copy.copy(i)
            j.name = "q" + j.name
            _temp.append(j)
        self.union_Fta.extend_States_list(_temp)


"""
Example of use  :
"""
if __name__== "__main__":
    symb = ranked_Alpha(name="f", rank=2)
    s= State(name="q1", final=False, init=False)
    t=State(name="q2", final=False, init=False)
    u=State(name="q3", final=False, init=False)
    st = []
    st.append(s)
    st.append(t)
    st.append(u)
    rule = ranked_Rule(symbol = symb)
    rule.input = st
    rule.output = u
    rules = []
    rules.append(rule)
    rules.append(rule)
    alpha = []
    alpha.append(symb)
    automaton = ranked_Fta(fta_name="fta1", alphabet=alpha, fta_states=st, transitions=rules)
    unionn = Union(automaton, automaton)
    unionn.nondeterministic_union()
    unionn.union_Fta.print_Fta()
