# engine/union/abstract_union.py

from abc import ABC, abstractmethod

class AbstractFtaUnion(ABC):
    """
    Abstract base class for FTA union that allows:
    - Different alphabets (Σ1 ∪ Σ2)
    - Automatic renaming of conflicting states
    """

    def __init__(self, fta1, fta2):
        self.fta1 = fta1
        self.fta2 = fta2

    def compute(self):
        """
        Template method to construct the union FTA.
        """
        # Step 1: compute union alphabet
        alphabet = self._build_alphabet()

        # Step 2: rename conflicting states
        fta1_states, fta2_states, state_map1, state_map2 = self._rename_conflicting_states()

        # Step 3: construct transitions
        transitions = self._build_transitions(state_map1, state_map2)

        # Step 4: final and initial states
        final_states = self._build_final_states(state_map1, state_map2)
        initial_states = self._build_initial_states(state_map1, state_map2)

        # Step 5: build the final FTA
        return self._build_fta(
            states=fta1_states.union(fta2_states),
            alphabet=alphabet,
            transitions=transitions,
            finals=final_states,
            initials=initial_states
        )

    # ---------- Hooks ----------

    @abstractmethod
    def _build_alphabet(self):
        """
        Build the union alphabet (Σ1 ∪ Σ2).
        """
        pass

    @abstractmethod
    def _rename_conflicting_states(self):
        """
        Rename states if there are conflicts between fta1 and fta2.
        Returns:
            fta1_states, fta2_states, state_map1, state_map2
        """
        pass

    @abstractmethod
    def _build_transitions(self, state_map1, state_map2):
        """
        Build transitions using the possibly renamed states.
        """
        pass

    @abstractmethod
    def _build_final_states(self, state_map1, state_map2):
        pass

    @abstractmethod
    def _build_initial_states(self, state_map1, state_map2):
        pass

    @abstractmethod
    def _build_fta(self, states, alphabet, transitions, finals, initials):
        """
        Factory method to create the concrete FTA object.
        """
        pass
