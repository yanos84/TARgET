# engine/union/ranked_union.py

from .abstract_union import AbstractFtaUnion
from fta.rankedfta import ranked_Fta
from fta.state import State
from fta.rankedRule import ranked_Rule


class RankedFtaUnion(AbstractFtaUnion):

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
        Returns:
            fta1_states, fta2_states, state_map1, state_map2
        """
        names1 = {s.name for s in self.fta1.states_list}
        names2 = {s.name for s in self.fta2.states_list}

        conflicts = names1.intersection(names2)

        state_map1 = {s: s for s in self.fta1.states_list}
        state_map2 = {}

        fta2_states = set()
        for s in self.fta2.states_list:
            if s.name in conflicts:
                new_name = f"2_{s.name}"
                new_state = State(new_name, final=s.is_Final, init=s.is_Initial)
                state_map2[s] = new_state
                fta2_states.add(new_state)
            else:
                state_map2[s] = s
                fta2_states.add(s)

        fta1_states = set(self.fta1.states_list)
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