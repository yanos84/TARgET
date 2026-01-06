from collections import defaultdict
from itertools import product
from engine.fta.determinism.semantics import BottomUpRankedSemantics
from engine.fta.determinism.determinism import Determinism
from engine.fta.minimization.abs_minimize import abs_minimize

class dfta_minimizer(abs_minimize):
    def __init__(self):
        super().__init__()



    def minimize(self, fta):
        semantics = BottomUpRankedSemantics()
        #is_deterministic = Determinism.check(fta.transitions, semantics)
        if not Determinism.check(fta.transitions, semantics):
            raise ValueError("FTA must be deterministic for minimization.")
        
        # Step 1: Initial partition
        final = {s for s in fta.states_list if s.is_Final}
        non_final = set(fta.states_list) - final
        partitions = [final, non_final]

        # Helper: find partition containing a state
        def get_partition_index(state):
            for i, p in enumerate(partitions):
                if state in p:
                    return i
            return None


        changed = True
        while changed:
            changed = False
            new_partitions = []
            for p in partitions:
                # split partition p if needed
                groups = defaultdict(set)
                for state in p:
                    key = []
                    for t in fta.transitions:
                        if t.output == state:
                            child_partitions = tuple(get_partition_index(q) for q in t.input)
                            key.append((t.func.name, child_partitions))
                    key = tuple(sorted(key))
                    groups[key].add(state)
                
                # If groups split, update
                if len(groups) > 1:
                    changed = True
                new_partitions.extend(groups.values())
            partitions = new_partitions

        # Step 2: Build new minimized FTA
        partition_states = {}
        for i, p in enumerate(partitions):
            # Name of the new state
            name = f"Q{i}"
            # Determine if it's final if any state in the partition is final
            is_final = any(s.is_Final for s in p)
            # Determine if initial if any state in the partition is initial
            is_initial = any(s.is_Initial for s in p)
            # Create new State object
            new_state = State(name, final=is_final, init=is_initial)
            # Map each old state in the partition to the new state
            for s in p:
                partition_states[s] = new_state

        # New states set
        new_states = set(partition_states.values())
        #new_final_states = {state_map[s] for s in fta.final_states}
        new_transitions = []
        for t in fta.transitions:
            new_inputs = [partition_states[q] for q in t.input]
            new_output = partition_states[t.output]
            new_transitions.append(t.__class__(t.func, new_inputs, new_output))
        
        # Create minimized FTA
        from fta.rankedfta import ranked_Fta
        minimized_fta = ranked_Fta(
            fta_name="fta1",
            alphabet=fta.alphabet,
            fta_states=new_states,
            #final_states=new_final_states,
            transitions=new_transitions)
        return minimized_fta


# Example usage
if __name__ == "__main__":
    from core.symbol import Ranked_Symbol
    from fta.state import State
    from fta.rankedfta import ranked_Fta
    from fta.rankedRule import ranked_Rule

    # Define states
    q0 = State("q0", final=False, init=True)
    q1 = State("q1", final=True, init=False)
    q2 = State("q2", final=True, init=False)

    # Define symbols
    f = Ranked_Symbol("f", rank=2)
    a = Ranked_Symbol("a", rank=0)

    # Define transitions
    r1 = ranked_Rule(f, [q0, q0], q1)
    r2 = ranked_Rule(f, [q1, q1], q1)
    r3 = ranked_Rule(f, [q0, q1], q2)
    r4 = ranked_Rule(a, [], q0)

    # Create FTA
    fta = ranked_Fta(
        fta_name="example_fta",
        alphabet=[f, a],
        fta_states=[q0, q1, q2],
        transitions=[r1, r2, r3, r4]
    )

    print("Original FTA:")
    fta.print_Fta()

    minimizer = dfta_minimizer()

    minimized_fta = minimizer.minimize(fta)

    print("\nMinimized FTA:")
    minimized_fta.print_Fta()