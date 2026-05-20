from .abs_emptiness import AbsEmptiness
from fta.rankedfta import ranked_Fta

class RankedEmptiness(AbsEmptiness):
    """Class to check the emptiness of a ranked finite tree automaton (RFTA).
    The emptiness of an RFTA is determined by checking if there are any states that can be reached from the initial states and lead to a final state through the transitions defined in the automaton. This is done by iteratively marking states as "good" if they can be reached from the initial states and can lead to a final state. If no final state can be marked as "good", then the automaton is considered empty.
    Attributes:
    - None
    Methods:
    - __init__: Initializes the RankedEmptiness class.
    - is_empty: Checks if the given ranked finite tree automaton is empty and returns a boolean value indicating the result.
    """
    def __init__(self):
        super().__init__()

    def is_empty(self, fta: ranked_Fta) -> bool:
        """Check if the ranked finite tree automaton is empty.
        Args:
            fta (ranked_Fta): The ranked finite tree automaton to check.
        Returns:
            bool: True if the automaton is empty, False otherwise.
        """

        Good = set()

        # Step 1: rank-0 rules
        for rule in fta.transitions:
            if rule.func.rank == 0:
                Good.add(rule.output_state.name)

        changed = True
        while changed:
            changed = False
            for rule in fta.transitions:
                if rule.func.rank > 0:
                    if all(s in Good for s in rule.input_states):
                        if rule.output_state.name not in Good:
                            Good.add(rule.output_state.name)
                            changed = True

        return Good.isdisjoint(fta.get_final_states())

#example usage
if __name__ == "__main__":
    from fta.rankedfta import ranked_Fta, Ranked_Symbol, ranked_Rule, State

    s= State(name="q1", is_Final=False)
    t=State(name="q2", is_Final=False)
    u=State(name="q3", is_Final=True)
    st = []
    st.append(s)
    st.append(t)
    symb = Ranked_Symbol(name="f", rank=2)
    rule = ranked_Rule(func = symb)
    rule.input_states = st
    rule.output_state = u
    rules = []
    rules.append(rule)
    alpha = []
    alpha.append(symb)
    automaton = ranked_Fta(fta_name="fta1", alphabet=alpha, fta_states=st, transitions=rules)
    emptiness_checker = RankedEmptiness()
    is_empty = emptiness_checker.is_empty(automaton)
    nada = ''
    if not is_empty:
        nada = 'not '
    print(f"The ranked finite tree automaton is {nada} empty")
