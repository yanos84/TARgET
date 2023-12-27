
from typing import List

import sys
sys.path.append('../TARgET/fta')

from fta import Fta


class Union():
    def __init__(self, A1, A2):
        self._A1: Fta= A1
        self._A2 : Fta = A2
        self.union_Fta = None

    def nondeterministic_ranked_union(self):
        for i in self._A1._states:
            self.union_Fta.append(i)


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
unionn.union_Fta.print_Fta()
