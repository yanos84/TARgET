from itertools import product
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.core.fta.rankedRule import ranked_Rule


def canonical_name(states):
    """
    Return a canonical string name encoding a subset of states.
    """
    return "{" + ",".join(sorted(s.name for s in states)) + "}"


def get_or_create_state(states, cache):
    """
    Return the deterministic state corresponding to a subset of states.
    """
    name = canonical_name(states)

    if name not in cache:
        cache[name] = State(
            name=name,
            is_Final=any(s.is_Final for s in states)
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
    Determinize a bottom-up ranked FTA using subset construction.

    Returns a deterministic FTA.
    """

    det_states_cache = {}
    det_rules = []
    worklist = []

    # --------------------------------------------------
    # Step 1: nullary transitions
    # --------------------------------------------------
    #
    # All transitions with the same nullary symbol must
    # be combined into one subset transition.
    #
    # Example:
    #     a() -> q0
    #     a() -> q1
    #
    # becomes:
    #     a() -> {q0,q1}
    #
    nullary_destinations = {}

    for rule in fta.transitions:
        if rule.func.rank == 0:
            nullary_destinations.setdefault(rule.func.name, []).append(
                rule.output_state
            )

    for symbol_name, destinations in nullary_destinations.items():

        # Retrieve the actual symbol object.
        symbol = next(
            symbol for symbol in fta.alphabet
            if symbol.name == symbol_name
        )

        # Remove duplicate states while preserving the subset semantics.
        destination_set = set(destinations)

        det_state = get_or_create_state(
            destination_set,
            det_states_cache
        )

        det_rule = ranked_Rule(
            func=symbol,
            input_states=[],
            output_state=det_state
        )

        if det_rule not in det_rules:
            det_rules.append(det_rule)

        if det_state not in worklist:
            worklist.append(det_state)

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

                for others in product(
                    det_states_cache.values(),
                    repeat=k - 1
                ):

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
                        output_subset,
                        det_states_cache
                    )

                    new_rule = ranked_Rule(
                        func=symbol,
                        input_states=list(children),
                        output_state=out_state
                    )

                    if new_rule not in det_rules:
                        det_rules.append(new_rule)

                    if out_state.name not in processed:
                        worklist.append(out_state)

    # --------------------------------------------------
    # Step 3: build deterministic FTA
    # --------------------------------------------------
    return ranked_Fta(
        fta_states=list(det_states_cache.values()),
        alphabet=fta.alphabet,
        transitions=det_rules
    )


# Example usage:*
if __name__ == "__main__":
    from TARgET.core.base.symbol import Ranked_Symbol
    q= State(name="q", is_Final=False)
    qg=State(name="qg", is_Final=False)
    qf=State(name="qf", is_Final=True)
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

#____ A second example 
 # States
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    # Symbols
    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    # Nondeterministic nullary transitions:
    #
    # a() -> q0
    # a() -> q1
    #
    rule1 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q0
    )

    rule2 = ranked_Rule(
        func=a,
        input_states=[],
        output_state=q1
    )

    # g(q0) -> qf
    rule3 = ranked_Rule(
        func=g,
        input_states=[q0],
        output_state=qf
    )

    fta = ranked_Fta(
        fta_states=[q0, q1, qf],
        alphabet=[a, g],
        transitions=[rule1, rule2, rule3]
    )

    print("Original FTA:")
    fta.print_Fta()

    print("\nDeterminized FTA:")
    determ_fta = determinize(fta)
    determ_fta.print_Fta()