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
    return ",".join(sorted(s.name for s in states))


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
    Used only during construction if needed.
    """
    return set(state.name.split(","))

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
            s = get_or_create_state([rule.output], det_states_cache)
            if s not in worklist:
                worklist.append(s)

    # --------------------------------------------------
    # Step 2: main worklist loop
    # --------------------------------------------------
    while worklist:
        current = worklist.pop()

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
                            if rule.input[i].name not in child_names:
                                ok = False
                                break

                        if ok:
                            output_subset.add(rule.output)

                    if not output_subset:
                        continue

                    out_state = get_or_create_state(
                        output_subset, det_states_cache
                    )

                    new_rule = ranked_Rule(
                        symbol=symbol,
                        input_states=list(children),
                        output_state=out_state
                    )

                    if new_rule not in det_rules:
                        det_rules.append(new_rule)

                    if out_state not in worklist:
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
    from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=5,
    seed=1234
)
    
    random_fta = generator.generate()
    random_fta.print_Fta()
    determ_fta = determinize(random_fta)
    determ_fta.print_Fta()