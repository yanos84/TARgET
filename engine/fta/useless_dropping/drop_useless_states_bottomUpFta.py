"""
This module implements the functionality to drop useless states from a finite tree automaton (FTA) using a bottom-up approach. Useless states are those that do not contribute to the acceptance of any tree, either because they cannot be reached from the initial states or because they cannot lead to a final state. The module defines functions to identify productive and reachable states, and then filters out the transitions that involve useless states. The resulting FTA will only contain states and transitions that are relevant for accepting trees, thus optimizing the automaton for further operations.   
The main functions in this module are:
    - productive_states(fta): Identifies and returns the set of productive states in the given FTA.
    - reachable_states(fta): Identifies and returns the set of reachable states in the given FTA.
    - drop_useless_states(fta): Modifies the given FTA by removing states that are not both productive and reachable, and returns the optimized FTA.
"""

def productive_states(fta):
    """
    Identify and return the set of productive states in the given finite tree automaton (FTA).
    A state is considered productive if it can lead to a final state through the transitions defined in the automaton. The function iteratively marks states as productive if they can reach a final state,"""
    productive = set()
    for s in fta.fta_states:
        if s.is_Final:
            productive.add(s)
    #productive = set(fta.final_states)
    changed = True

    while changed:
        changed = False
        for rule in fta.transitions:
            # if the output is productive,
            # then its inputs are productive
            if rule.output_state in productive:
                for q in rule.input_states:
                    if q not in productive:
                        productive.add(q)
                        changed = True

    return productive

def reachable_states(fta):
    """
    Identify and return the set of reachable states in the given finite tree automaton (FTA).
    A state is considered reachable if it can be reached from the initial states through the transitions defined in the automaton. The function iteratively marks states as reachable if they can be reached from the"""
    reachable = set()
    changed = True

    # arity-0 rules (constants)
    for rule in fta.transitions:
        if rule.func.rank == 0:
            reachable.add(rule.output_state)

    while changed:
        changed = False
        for rule in fta.transitions:
            if all(q in reachable for q in rule.input_states):
                if rule.output_state not in reachable:
                    reachable.add(rule.output_state)
                    changed = True

    return reachable

def drop_useless_states(fta):
    """
    Modify the given finite tree automaton (FTA) by removing states that are not both productive and reachable.
    The function identifies productive and reachable states, and then filters out transitions that involve useless states.
    The resulting FTA will only contain states and transitions that are relevant for accepting trees, optimizing the automaton for further operations.
    """ 
    productive = productive_states(fta)
    reachable = reachable_states(fta)

    useful = productive & reachable

    # filter states
    #fta.states = {q for q in fta.states if q in useful}

    # filter final states
    #fta.final_states = {q for q in fta.final_states if q in useful}

    # filter transitions
    new_transitions = []
    for rule in fta.transitions:
        if rule.output_state in useful and all(q in useful for q in rule.input_states):
            new_transitions.append(rule)

    fta.transitions = new_transitions

    return fta


# Example usage
if __name__ == "__main__":
    from core.symbol import Ranked_Symbol
    from fta.state import State
    from fta.rankedfta import ranked_Fta
    from fta.rankedRule import ranked_Rule

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