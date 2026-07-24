# impmlementation of ranked finite tree automata
# The class imports ranked alphabets and ascendent rules. On can define ascendency or descendency in the acceptor engine.


from .abst_fta import Fta
from .state import State
from ..base.symbol import Ranked_Symbol
from .rankedRule import ranked_Rule
from typing import List
from ..algebraic.semiring import Semiring

class ranked_Fta(Fta):

    """
    Class for ranked finite tree automata
    Inherits from Fta class
    Attributes:
    - alphabet: List of Ranked_Symbol objects representing the ranked alphabet of the automaton
    - transitions: List of ranked_Rule objects representing the transition rules of the automaton
    Methods:
    - __init__: Constructor to initialize the ranked finite tree automaton with a name, alphabet, states, and transitions
    - print_Fta: Method to print the details of the ranked finite tree automaton    
    """

    def __init__(self, fta_name='default_fta', alphabet:List[Ranked_Symbol]= None, fta_states:List[State]=None, transitions : List[ranked_Rule]=None):
        """
        Initializes a ranked finite tree automaton with the given name, alphabet, states, and transitions.
        :param fta_name: The name of the finite tree automaton (default is 'default_fta').
        :param alphabet: A list of Ranked_Symbol objects representing the ranked alphabet of the automaton (default is None).
        :param fta_states: A list of State objects representing the states of the automaton (default is None).
        :param transitions: A list of ranked_Rule objects representing the transition rules of the automaton (default is None).
        """
        super().__init__(fta_name,fta_states)
        self.alphabet : List[Ranked_Symbol] = alphabet
        self.transitions : List[ranked_Rule] = transitions

    def print_Fta(self):
        """
        Prints the details of the ranked finite tree automaton, including its name, states, alphabet, and transition rules.
        """

        print("Fta name: "+self.name)
        print("States list: "+' '.join([i.name+" (is final :"+ str(i.is_Final)+"), " for i in self.fta_states])[:-1])
        print("Alphabet: "+' '.join([i.name+ "(rank = "+ str(i.rank)+"), " for i in self.alphabet ])[:-1])
        print("Rules list:\n "+ ' '.join([i.get_rule_as_str()+"\n" for i in self.transitions]))

    def __str__(self):
        """
        Returns a string representation of the ranked finite tree automaton, including its name, states, alphabet, and transition rules.
        :return: A string representation of the ranked finite tree automaton.
        """
        _name = "Fta name: "+self.name+"\n"
        _states = "States list: "+' '.join([i.name+" (is final :"+ str(i.is_Final)+"), " for i in self.fta_states])[:-1]+"\n"
        _alphabet = "Alphabet: "+' '.join([i.name+ "(rank = "+ str(i.rank)+"), " for i in self.alphabet ])[:-1]+"\n"
        _rules = "Rules list:\n "+ ' '.join([i.get_rule_as_str()+"\n" for i in self.transitions])+"\n"
        return _name+_states+_alphabet+_rules   
    
    def chech_weighted(self)->bool:
        """
        Checks if all transitions in the ranked finite tree automaton are weighted or not.
        :return: True if all transitions are weighted, False if none are weighted, raises ValueError if there is a mix of weighted and unweighted transitions.
        """
        if all(r.is_weighted for r in self.transitions):
            return True
        elif not any(r.is_weighted for r in self.transitions):
            return False
        else:
            raise ValueError("Check fta transitions, Some are weighted and some are not (this is to avoid using semiring.one and consider all transitiosn as weighted)")

    def get_semiring(self):
        """
        Returns the semiring type of the weighted transitions in the ranked finite tree automaton.
        :return: The semiring type of the weighted transitions.
        :raises ValueError: If the automaton is unweighted or if there are multiple semiring types.
        """
        if self.chech_weighted():
            _semirings = {type(t.weight) for t in self.transitions}
            if len(_semirings)!=1:
                raise ValueError("Check your transitions: multiple semiring types detected")
            else:
                return _semirings.pop()
        else:
            raise ValueError("You are triying to use an unweighted Fta as weighted one")



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
