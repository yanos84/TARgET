# impmlementation of ranked finite tree automata
# The class imports ranked alphabets and ascendent rules. On can define ascendency or descendency in the acceptor engine.


from fta import Fta
from state import State
from alphabet import ranked_Alpha
from rankedRule import ranked_Rule
from typing import List

class ranked_Fta(Fta):

    #Define constructor

    def __init__(self, fta_name=None, alphabet:List[ranked_Alpha]= None, fta_states:List[State]=None, transitions : List[ranked_Rule]=None):
        super().__init__(fta_name,fta_states)
        self.alphabet : List[ranked_Alpha] = alphabet
        self.transitions : List[ranked_Rule] = transitions

    def print_Fta(self):
        print("Fta name: "+self.name)
        print("States list: "+' '.join([i.name+" (is final :"+ str(i.is_Final)+"), " for i in self.states_list])[:-1])
        print("Alphabet: "+' '.join([i.name+ "(rank = "+ str(i.rank)+"), " for i in self.alphabet ])[:-1])
        print("Rules list:\n "+ ' '.join([i.get_rule_as_str()+"\n" for i in self.transitions]))

"""
-------------Testing -------------------------------------------------------
"""

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
