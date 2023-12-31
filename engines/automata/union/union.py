
from typing import List

import sys
sys.path.append('../TARgET/fta')
sys.path.append('../TARgET/.fta')

from fta import Fta
from state import State
from alphabet import ranked_Alpha
from rankedRule import ranked_Rule
from rankedfta import ranked_Fta

class Union():
    def __init__(self, A1, A2):
        self._A1: Fta= A1
        self._A2 : Fta = A2
        self.union_Fta : ranked_Fta = ranked_Fta(fta_states = [])

    def nondeterministic_union(self):
        self.union_Fta.name = "Union"+self._A1.name+self._A2.name
        #self.union_Fta.
        """for i in self._A1.states_list:
            self.union_Fta.add_state(i)
        for i in self._A2.states_list:
            self.union_Fta.add_state(i)"""
        self.union_Fta.extend_States_list(self._A1.states_list)
        self.union_Fta.extend_States_list(self._A2.states_list)
        print(self.union_Fta.states_list)


symb = ranked_Alpha(name="f", rank=2)
s= State(name="q1", final=False, init=False)
t=State(name="q2", final=False, init=False)
u=State(name="q3", final=False, init=False)
st = []
st.append(s)
st.append(t)
rule = ranked_Rule(symbol = symb)
rule.input = st
rule.output = u
rules = []
rules.append(rule)
rules.append(rule)
alpha = []
alpha.append(symb)
automaton = ranked_Fta(fta_name="fta1", alphabet=alpha, fta_states=st, transitions=rules)
automaton.print_Fta()
unionn = Union(automaton, automaton)
unionn.nondeterministic_union()
unionn.union_Fta.print_Fta()
