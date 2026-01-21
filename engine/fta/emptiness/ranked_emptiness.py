from .abs_emptiness import AbsEmptiness
from fta.rankedfta import ranked_Fta

class RankedEmptiness(AbsEmptiness):
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

    s= State(name="q1", final=False)
    t=State(name="q2", final=False)
    u=State(name="q3", final=True)
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
