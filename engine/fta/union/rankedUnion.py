# engine/union/ranked_union.py

from .abstract_union import AbstractFtaUnion
from TARgET.fta.rankedfta import ranked_Fta
from TARgET.fta.state import State
from TARgET.fta.rankedRule import ranked_Rule


class RankedFtaUnion(AbstractFtaUnion):
    """Class to compute the union of two ranked finite tree automata (RFTAs).
    The union of two RFTAs, RFTA1 and RFTA2, is a new RFTA that accepts exactly the trees that are accepted by either RFTA1 or RFTA2. This is achieved by constructing a new RFTA that combines the states and transitions of both RFT
    As while ensuring that the acceptance conditions reflect the union of the languages accepted by the original RFTAs. The resulting union RFTA can be used to check for acceptance of trees in either RFTA1 or RFTA2, or to perform operations like intersection and difference with other RFTAs.
    Attributes:
        - fta1: The first ranked finite tree automaton for the union operation.
        - fta2: The second ranked finite tree automaton for the union operation.
    Methods:
        - __init__: Initializes the RankedFtaUnion class with two RFTAs.
        - compute: Computes the union of the two RFTAs and returns a new RFTA representing the union.
        - _build_alphabet: Builds the alphabet for the union RFTA by taking the union of the alphabets of the two input RFTAs.
        - _rename_conflicting_states: Renames states to avoid collisions between the two input RFTAs and returns the updated states and state mappings.
        - _build_transitions: Builds the transitions for the union RFTA by mapping the transitions of the two input RFTAs according to the state mappings.
        - _build_final_states: Builds the set of final states for the union RFTA by combining the final states of the two input RFTAs.
        - _build_initial_states: Builds the set of initial states for the union RFTA by combining the initial states of the two input RFTAs.
        - _build_fta: Constructs the final union RFTA using the computed states, alphabet, transitions, final states, and initial states.
    """

    def _build_alphabet(self):
        # Union of both alphabets
        union_alpha_list = []
        for symbol in self.fta1.alphabet+self.fta2.alphabet:
            if symbol not in union_alpha_list:
                union_alpha_list.append(symbol)
        return union_alpha_list
        #return self.fta1.alphabet.union(self.fta2.alphabet)

    def _rename_conflicting_states(self):
        """
        Rename states to avoid collisions.

        :returns: A tuple containing the renamed state sets and the corresponding state mappings: ``(fta1_states, fta2_states, state_map1, state_map2)``.
        :rtype: tuple
        """
        names1 = {s.name for s in self.fta1.fta_states}
        names2 = {s.name for s in self.fta2.fta_states}

        conflicts = names1.intersection(names2)

        state_map1 = {s: s for s in self.fta1.fta_states}
        state_map2 = {}

        fta2_states = set()
        for s in self.fta2.fta_states:
            if s.name in conflicts:
                new_name = f"2_{s.name}"
                new_state = State(new_name, is_Final=s.is_Final, is_Initial=s.is_Initial)
                state_map2[s] = new_state
                fta2_states.add(new_state)
            else:
                state_map2[s] = s
                fta2_states.add(s)

        fta1_states = set(self.fta1.fta_states)
        return fta1_states, fta2_states, state_map1, state_map2

    def _build_transitions(self, state_map1, state_map2):
        """
        Build union transitions, renaming states if needed
        """
        transitions = set()

        # map fta1 transitions
        for r in self.fta1.transitions:
            new_input_states = [state_map1[s] for s in r.input_states]
            new_output_state = state_map1[r.output_state]
            transitions.add(ranked_Rule(r.func, new_input_states, new_output_state))

        # map fta2 transitions
        for r in self.fta2.transitions:
            new_input_states = [state_map2[s] for s in r.input_states]
            new_output_state = state_map2[r.output_state]
            transitions.add(ranked_Rule(r.func, new_input_states, new_output_state))

        return transitions

    def _build_final_states(self, state_map1, state_map2):
        finals = {s for s in state_map1.values() if s.is_Final}
        finals.update({s for s in state_map2.values() if s.is_Final})
        return finals

    def _build_initial_states(self, state_map1, state_map2):
        initials = {s for s in state_map1.values() if s.is_Initial}
        initials.update({s for s in state_map2.values() if s.is_Initial})
        return initials

    def _build_fta(self, states, alphabet, transitions, finals, initials):
        return ranked_Fta(
            fta_name=f"Union_of_{self.fta1.name}_and_{self.fta2.name}",
            fta_states=states,
            alphabet=alphabet,
            transitions=transitions
        )


# Example usage:*
if __name__ == "__main__":
    from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    generator2 = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    random_fta = generator.generate()
    random_fta2 = generator2.generate()
    union_builder = RankedFtaUnion(random_fta, random_fta2)
    union_fta = union_builder.compute()
    union_fta.print_Fta()