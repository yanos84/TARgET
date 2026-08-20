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

    def __eq__(self, other):
        """
        Tests equality of two ranked finite tree automata independently
        of state names.

        Two FTAs are equal if they have the same alphabet and there exists
        a bijection between their states preserving:
        - final status;
        - initial status;
        - transition structure.
        """
        if not isinstance(other, ranked_Fta):
            return NotImplemented

        # FTA names are irrelevant.
        if set(self.alphabet) != set(other.alphabet):
            return False

        if len(self.fta_states) != len(other.fta_states):
            return False

        if len(self.transitions) != len(other.transitions):
            return False

        # Try all possible state mappings.
        from itertools import permutations

        for permutation in permutations(other.fta_states):
            state_map = dict(zip(self.fta_states, permutation))

            # Preserve state properties.
            if any(
                s.is_Final != state_map[s].is_Final
                or s.is_Initial != state_map[s].is_Initial
                for s in self.fta_states
            ):
                continue

            # Compare transitions structurally.
            valid = True

            for rule in self.transitions:

                # Find a corresponding rule in other.
                found = False

                for other_rule in other.transitions:

                    if rule.func != other_rule.func:
                        continue

                    if len(rule.input_states) != len(other_rule.input_states):
                        continue

                    if any(
                        state_map[s1] != s2
                        for s1, s2 in zip(
                            rule.input_states,
                            other_rule.input_states
                        )
                    ):
                        continue

                    if state_map[rule.output_state] != other_rule.output_state:
                        continue

                    # If weighted, also compare weights.
                    if rule.is_weighted != other_rule.is_weighted:
                        continue

                    if (
                        rule.is_weighted
                        and rule.weight != other_rule.weight
                    ):
                        continue

                    found = True
                    break

                if not found:
                    valid = False
                    break

            if valid:
                return True

        return False

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
    
    def chech_weighted(self) -> bool:
        if not self.transitions:
            return False

        if all(r.is_weighted for r in self.transitions):
            return True
        elif not any(r.is_weighted for r in self.transitions):
            return False
        else:
            raise ValueError(
                "Check fta transitions, Some are weighted and some are not "
                "(this is to avoid using semiring.one and consider all "
                "transitions as weighted)"
            )


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

def test_fta_equal_with_different_state_names():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 1)

    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)

    r0 = State("r0", is_Final=False)
    r1 = State("r1", is_Final=True)

    rule1 = ranked_Rule(func=a)
    rule1.input_states = []
    rule1.output_state = q0

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [q0]
    rule2.output_state = q1

    rule3 = ranked_Rule(func=a)
    rule3.input_states = []
    rule3.output_state = r0

    rule4 = ranked_Rule(func=f)
    rule4.input_states = [r0]
    rule4.output_state = r1

    fta1 = ranked_Fta(
        fta_name="fta1",
        alphabet=[a, f],
        fta_states=[q0, q1],
        transitions=[rule1, rule2],
    )

    fta2 = ranked_Fta(
        fta_name="fta2",
        alphabet=[a, f],
        fta_states=[r0, r1],
        transitions=[rule3, rule4],
    )

    assert fta1 == fta2

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
    test_fta_equal_with_different_state_names()
