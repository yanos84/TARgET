# impmlementation of ranked finite tree automata
# The class imports ranked alphabets and ascendent rules. On can define ascendency or descendency in the acceptor engine.


from .abst_fta import Fta
from .state import State
from core.symbol import Ranked_Symbol
from .rankedRule import ranked_Rule
from typing import List

class ranked_Fta(Fta):

    '''
    Class for ranked finite tree automata
    Inherits from Fta class
    Attributes:
    - alphabet: List of Ranked_Symbol objects representing the ranked alphabet of the automaton
    - transitions: List of ranked_Rule objects representing the transition rules of the automaton
    Methods:
    - __init__: Constructor to initialize the ranked finite tree automaton with a name, alphabet, states, and transitions
    - print_Fta: Method to print the details of the ranked finite tree automaton    
    '''

    def __init__(self, fta_name='default_fta', alphabet:List[Ranked_Symbol]= None, fta_states:List[State]=None, transitions : List[ranked_Rule]=None):
        super().__init__(fta_name,fta_states)
        self.alphabet : List[Ranked_Symbol] = alphabet
        self.transitions : List[ranked_Rule] = transitions

    def print_Fta(self):
        print("Fta name: "+self.name)
        print("States list: "+' '.join([i.name+" (is final :"+ str(i.is_Final)+"), " for i in self.states_list])[:-1])
        print("Alphabet: "+' '.join([i.name+ "(rank = "+ str(i.rank)+"), " for i in self.alphabet ])[:-1])
        print("Rules list:\n "+ ' '.join([i.get_rule_as_str()+"\n" for i in self.transitions]))

    def __str__(self):
        _name = "Fta name: "+self.name+"\n"
        _states = "States list: "+' '.join([i.name+" (is final :"+ str(i.is_Final)+"), " for i in self.states_list])[:-1]+"\n"
        _alphabet = "Alphabet: "+' '.join([i.name+ "(rank = "+ str(i.rank)+"), " for i in self.alphabet ])[:-1]+"\n"
        _rules = "Rules list:\n "+ ' '.join([i.get_rule_as_str()+"\n" for i in self.transitions])+"\n"
        return _name+_states+_alphabet+_rules   

"""
-------------Testing -------------------------------------------------------
"""


#Example usage

if __name__ == "__main__":

    s= State(name="q1", is_Final=False, is_Initial=False)
    t=State(name="q2", is_Final=False, is_Initial=False)
    u=State(name="q3", is_Final=False, is_Initial=False)
    st = []
    st.append(s)
    st.append(t)
    symb = Ranked_Symbol(name="f", rank=2)
    rule = ranked_Rule(func = symb)
    rule.input_states = st
    rule.output_state = u
    rules = []
    rules.append(rule)
    rules.append(rule)
    alpha = []
    alpha.append(symb)
    automaton = ranked_Fta(fta_name="fta1", alphabet=alpha, fta_states=st, transitions=rules)
    automaton.print_Fta()
