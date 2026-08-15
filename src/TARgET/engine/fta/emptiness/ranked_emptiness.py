from .abs_emptiness import AbsEmptiness
from TARgET.core.fta.rankedfta import ranked_Fta


from .abs_emptiness import AbsEmptiness
from TARgET.core.fta.rankedfta import ranked_Fta


class RankedEmptiness(AbsEmptiness):
    """Class to check if a ranked finite tree automaton is empty."""

    def __init__(self):
        super().__init__()

    def is_empty(self, fta: ranked_Fta) -> bool:
        """
        Check whether a ranked finite tree automaton recognizes the empty language.

        :param fta: The ranked finite tree automaton to check.

        :returns: ``True`` if the automaton recognizes the empty language;
            otherwise, ``False``.
        """

        # Good contains the names of states that can be reached
        # by some ground tree.
        good = set()

        # Step 1: rank-0 rules
        for rule in fta.transitions:
            if rule.func.rank == 0:
                good.add(rule.output_state.name)

        # Step 2: propagate reachable states
        changed = True
        while changed:
            changed = False

            for rule in fta.transitions:
                if rule.func.rank > 0:
                    if all(state.name in good for state in rule.input_states):
                        if rule.output_state.name not in good:
                            good.add(rule.output_state.name)
                            changed = True

        # get_final_states() returns state names.
        final_states = set(fta.get_final_states())

        # The language is empty if no final state is reachable.
        return good.isdisjoint(final_states)

#example usage

def test_non_empty_rfta_with_nested_tree():
    # States
    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    # Symbols
    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    # a() -> q0
    rule_a = ranked_Rule(func=a)
    rule_a.input_states = []
    rule_a.output_state = q0

    # g(q0) -> qf
    rule_g = ranked_Rule(func=g)
    rule_g.input_states = [q0]
    rule_g.output_state = qf

    # Automaton
    automaton = ranked_Fta(
        fta_name="non_empty_test",
        alphabet=[a, g],
        fta_states=[q0, qf],
        transitions=[rule_a, rule_g],
    )

    # Test
    #emptiness_checker = RankedEmptiness()
    #print(emptiness_checker.is_empty(automaton))  # Should print False

    assert emptiness_checker.is_empty(automaton) is False

if __name__ == "__main__":
    from TARgET.core.fta.rankedfta import ranked_Fta, Ranked_Symbol, ranked_Rule, State

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

#______second example _________
    # States
    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    # Symbols
    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    # Rules:
    # a() -> q0
    rule_a = ranked_Rule(func=a)
    rule_a.input_states = []
    rule_a.output_state = q0

    # g(q0) -> qf
    rule_g = ranked_Rule(func=g)
    rule_g.input_states = [q0]
    rule_g.output_state = qf

    automaton = ranked_Fta(
        fta_name="non_empty_test",
        alphabet=[a, g],
        fta_states=[q0, qf],
        transitions=[rule_a, rule_g],
    )

    emptiness_checker = RankedEmptiness()
    is_empty = emptiness_checker.is_empty(automaton)

    if is_empty:
        print("The ranked finite tree automaton is empty")
    else:
        print("The ranked finite tree automaton is not empty")


