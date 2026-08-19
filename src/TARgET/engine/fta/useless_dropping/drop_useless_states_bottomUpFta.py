"""
This module implements the functionality to drop useless states from a finite tree automaton (FTA) using a bottom-up approach. Useless states are those that do not contribute to the acceptance of any tree, either because they cannot be reached from the initial states or because they cannot lead to a final state. The module defines functions to identify productive and reachable states, and then filters out the transitions that involve useless states. The resulting FTA will only contain states and transitions that are relevant for accepting trees, thus optimizing the automaton for further operations.   
The main functions in this module are:
    - productive_states(fta): Identifies and returns the set of productive states in the given FTA.
    - reachable_states(fta): Identifies and returns the set of reachable states in the given FTA.
    - drop_useless_states(fta): Modifies the given FTA by removing states that are not both productive and reachable, and returns the optimized FTA.
"""

def productive_states(fta):
    """
    Return the states that can contribute to an accepted tree.

    A state is productive if it can derive a tree that eventually
    reaches a final state.
    """
    productive = {
        state
        for state in fta.fta_states
        if state.is_Final
    }

    changed = True

    while changed:
        changed = False

        for rule in fta.transitions:
            if rule.output_state in productive:
                for state in rule.input_states:
                    if state not in productive:
                        productive.add(state)
                        changed = True

    return productive


def reachable_states(fta):
    """
    Return the states reachable by some ground tree.

    For a bottom-up FTA, reachability starts from the outputs of
    nullary transitions and propagates bottom-up through transitions.
    """
    reachable = set()

    # Nullary symbols generate the initial reachable states.
    for rule in fta.transitions:
        if rule.func.rank == 0:
            reachable.add(rule.output_state)

    changed = True

    while changed:
        changed = False

        for rule in fta.transitions:
            if all(
                state in reachable
                for state in rule.input_states
            ):
                if rule.output_state not in reachable:
                    reachable.add(rule.output_state)
                    changed = True

    return reachable


def drop_useless_states(fta):
    """
    Remove all states that are either unreachable or non-productive.

    A useful state must be both:
      - reachable by some ground tree, and
      - productive toward a final state.

    The FTA is modified in place and returned.
    """
    productive = productive_states(fta)
    reachable = reachable_states(fta)

    useful = productive & reachable

    # Remove useless states.
    fta.fta_states = [
        state
        for state in fta.fta_states
        if state in useful
    ]

    # Remove transitions involving useless states.
    fta.transitions = [
        rule
        for rule in fta.transitions
        if (
            rule.output_state in useful
            and all(
                state in useful
                for state in rule.input_states
            )
        )
    ]

    return fta


# Example usage
if __name__ == "__main__":
    from TARgET.core.base.symbol import Ranked_Symbol
    from TARgET.core.fta.state import State
    from TARgET.core.fta.rankedfta import ranked_Fta
    from TARgET.core.fta.rankedRule import ranked_Rule

    q= State(name="q", is_Final=False)
    qg=State(name="qg", is_Final=False)
    qf=State(name="qf", is_Final=True)
    q_useless=State(name="quseless", is_Final=False)
    symb_f = Ranked_Symbol(name="f", rank=2)
    symb_a = Ranked_Symbol(name="a", rank=0)
    symb_g = Ranked_Symbol(name="g", rank=1)
    rule1 = ranked_Rule(func = symb_a, input_states=[], output_state=q)
    rule2 = ranked_Rule(func = symb_g, input_states=[q], output_state=qg)
    rule3 = ranked_Rule(func = symb_f, input_states=[q, q], output_state=q)
    rule4 = ranked_Rule(func = symb_g, input_states=[q], output_state=q)
    rule5 = ranked_Rule(func = symb_g, input_states=[qg], output_state=qf)
    useless_rule = ranked_Rule(func = symb_a, input_states=[], output_state=q_useless)

    fta = ranked_Fta(
    fta_states=[q, qg, qf],
    alphabet=[symb_a, symb_g, symb_f],
    transitions=[rule1, rule2, rule3, rule4, rule5, useless_rule]
)
    print("Before dropping useless states:")
    fta.print_Fta()
    drop_useless_states(fta)
    print("After dropping useless states:")
    fta.print_Fta()