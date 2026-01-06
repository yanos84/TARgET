def productive_states(fta):
    productive = set()
    for s in fta.states_list:
        if s.is_Final:
            productive.add(s)
    #productive = set(fta.final_states)
    changed = True

    while changed:
        changed = False
        for rule in fta.transitions:
            # if the output is productive,
            # then its inputs are productive
            if rule.output in productive:
                for q in rule.input:
                    if q not in productive:
                        productive.add(q)
                        changed = True

    return productive

def reachable_states(fta):
    reachable = set()
    changed = True

    # arity-0 rules (constants)
    for rule in fta.transitions:
        if rule.func.rank == 0:
            reachable.add(rule.output)

    while changed:
        changed = False
        for rule in fta.transitions:
            if all(q in reachable for q in rule.input):
                if rule.output not in reachable:
                    reachable.add(rule.output)
                    changed = True

    return reachable

def drop_useless_states(fta):
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
        if rule.output in useful and all(q in useful for q in rule.input):
            new_transitions.append(rule)

    fta.transitions = new_transitions

    return fta


# Example usage
if __name__ == "__main__":
    from core.symbol import Ranked_Symbol
    from fta.state import State
    from fta.rankedfta import ranked_Fta
    from fta.rankedRule import ranked_Rule

    q= State(name="q", final=False, init=False)
    qg=State(name="qg", final=False, init=False)
    qf=State(name="qf", final=True, init=False)
    q_useless=State(name="quseless", final=False, init=False)
    symb_f = Ranked_Symbol(name="f", rank=2)
    symb_a = Ranked_Symbol(name="a", rank=0)
    symb_g = Ranked_Symbol(name="g", rank=1)
    rule1 = ranked_Rule(symbol = symb_a, input_states=[], output_state=q)
    rule2 = ranked_Rule(symbol = symb_g, input_states=[q], output_state=qg)
    rule3 = ranked_Rule(symbol = symb_f, input_states=[q, q], output_state=q)
    rule4 = ranked_Rule(symbol = symb_g, input_states=[q], output_state=q)
    rule5 = ranked_Rule(symbol = symb_g, input_states=[qg], output_state=qf)
    useless_rule = ranked_Rule(symbol = symb_a, input_states=[], output_state=q_useless)

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