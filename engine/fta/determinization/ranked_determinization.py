from itertools import product
from fta.rankedfta import ranked_Fta
from fta.state import State
from fta.rankedRule import ranked_Rule
from typing import List


def canonical_name(states):
    """
    states: iterable[State]
    returns: canonical string name encoding the subset
    """
    return "{" + ",".join(sorted(s.name for s in states)) + "}"


def get_or_create_state(states, cache):
    """
    states: iterable[State]
    cache: dict[str, State]
    """
    name = canonical_name(states)
    if name not in cache:
        cache[name] = State(
            name=name,
            final=any(s.is_Final for s in states)
        )
    return cache[name]


def decode_state(state):
    """
    Extract original state names from a deterministic state name.
    """
    name = state.name.strip()
    if name == "{}":
        return set()
    return set(name[1:-1].split(","))


def determinize(fta):
    """
    Determinize a bottom-up ranked FTA using canonical state names.
    Returns a deterministic FTA with standard State and Rule objects.
    """

    det_states_cache = {}     # name -> State
    det_rules = []
    worklist = []

    # --------------------------------------------------
    # Step 1: base states (nullary transitions)
    # --------------------------------------------------
    for rule in fta.transitions:
        if rule.func.rank == 0:
            s = get_or_create_state([rule.output_state], det_states_cache)

            det_rule = ranked_Rule(
                func=rule.func,
                input_states=[],
                output_state=s
            )

            if det_rule not in det_rules:
                det_rules.append(det_rule)

            if s not in worklist:
                worklist.append(s)
        # --------------------------------------------------
    # Step 2: main worklist loop
    # --------------------------------------------------
    processed = set()
    while worklist:
        current = worklist.pop()
        if current.name in processed:
            continue
        processed.add(current.name)

        for symbol in fta.alphabet:
            k = symbol.rank
            if k == 0:
                continue

            # current participates at each argument position
            for pos in range(k):
                for others in product(det_states_cache.values(), repeat=k-1):

                    children = list(others)
                    children.insert(pos, current)
                    children = tuple(children)

                    output_subset = set()

                    for rule in fta.transitions:
                        if rule.func != symbol:
                            continue

                        ok = True
                        for i in range(k):
                            child_names = decode_state(children[i])
                            if rule.input_states[i].name not in child_names:
                                ok = False
                                break

                        if ok:
                            output_subset.add(rule.output_state)

                    if not output_subset:
                        continue

                    out_state = get_or_create_state(
                        output_subset, det_states_cache
                    )

                    new_rule = ranked_Rule(
                        func=symbol,
                        input_states=list(children),
                        output_state=out_state
                    )

                    if new_rule not in det_rules:
                        det_rules.append(new_rule)

                    if out_state not in processed:
                        worklist.append(out_state)



    # --------------------------------------------------
    # Step 3: build deterministic FTA
    # --------------------------------------------------
    return ranked_Fta(
        fta_states=list(det_states_cache.values()),
        alphabet=fta.alphabet,
        transitions=det_rules,
        #finals=[s for s in det_states_cache.values() if s.final]
    )



# Example usage:*
if __name__ == "__main__":
    from core.symbol import Ranked_Symbol
    q= State(name="q", final=False, init=False)
    qg=State(name="qg", final=False, init=False)
    qf=State(name="qf", final=True, init=False)
    symb_f = Ranked_Symbol(name="f", rank=2)
    symb_a = Ranked_Symbol(name="a", rank=0)
    symb_g = Ranked_Symbol(name="g", rank=1)
    rule1 = ranked_Rule(func= symb_a, input_states=[], output_state=q)
    rule2 = ranked_Rule(func = symb_g, input_states=[q], output_state=qg)
    rule3 = ranked_Rule(func = symb_f, input_states=[q, q], output_state=q)
    rule4 = ranked_Rule(func = symb_g, input_states=[q], output_state=q)
    rule5 = ranked_Rule(func = symb_g, input_states=[qg], output_state=qf)

    fta = ranked_Fta(
        fta_states=[q, qg, qf],
        alphabet=[symb_a, symb_g, symb_f],
        transitions=[rule1, rule2, rule3, rule4, rule5]
    )

    determ_fta = determinize(fta)
    determ_fta.print_Fta()