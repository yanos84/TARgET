from collections import defaultdict
from engine.fta.determinism.semantics import BottomUpRankedSemantics
from engine.fta.determinism.determinism import Determinism
from engine.fta.minimization.abs_minimize import abs_minimize
from fta.rankedRule import ranked_Rule
from fta.rankedfta import ranked_Fta
from fta.state import State

class dfta_minimizer(abs_minimize):
    '''
    Minimizer for Deterministic Finite Tree Automata (DFTA) using
    a standard partition refinement algorithm. 
    '''

    def __init__(self):
        super().__init__()


    def check_determinism(self, fta)->ranked_Fta:
        '''
        Check if the given FTA is deterministic using BottomUpRankedSemantics class. 
        '''
        semantics = BottomUpRankedSemantics()
        return Determinism.check(fta.transitions, semantics)

    def get_final_states(self, fta):
        '''
        Return the set of final states of the given FTA.
        '''
        return {s for s in fta.states_list if s.is_Final}
    
    def get_partition_index(self, partitions, state):
        '''
        Return the index of the partition (of sets of states) containing the given state.
        '''
        for i, p in enumerate(partitions):
            if state in p:
                return i
        return None
    
    def redendant_rules(self, rule:ranked_Rule, transitions: set)->bool:
        '''
        Check if a given rule is redundant in a set of transitions.
        '''
        for r in transitions:
            if rule == r:
                return True
        return False


    def minimize(self, fta):
        '''
        Minimize the given deterministic FTA using partition refinement.
        Returns a new minimized DFTA.
        '''
        #is_deterministic = Determinism.check(fta.transitions, semantics)
        if not self.check_determinism(fta):
            raise ValueError("FTA must be deterministic for minimization.")
        
        # Step 1: Initial partition
        final = self.get_final_states(fta)
        non_final = set(fta.states_list) - final
        partitions = [final, non_final]
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
                        if state in t.input:
                            child_partitions = tuple(self.get_partition_index(partitions, q) for q in t.input)
                            output_partition = self.get_partition_index(partitions, t.output)
                            key.append((t.func.name, child_partitions, output_partition))
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
            if not self.redendant_rules(t.__class__(t.func, new_inputs, new_output), new_transitions):
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
    from engine.utils.rankedFta_xml_import import load_fta_from_xml
    fta = load_fta_from_xml("dfta_for_minim.xml")

    print("Original FTA:")
    fta.print_Fta()
    print("Original FTA:")
    fta.print_Fta()

    minimizer = dfta_minimizer()

    minimized_fta = minimizer.minimize(fta)

    print("\nMinimized FTA:")
    minimized_fta.print_Fta()