from .acceptor import Acceptor
from TARgET.fta.rankedfta import ranked_Fta
from TARgET.core.rankedTree import RankedTree
from TARgET.fta.state import State
from typing import Set

class RankedBottomUpAcceptor(Acceptor):
    """
    Bottom-up acceptance algorithm for ranked finite tree automata.
    Implements a bottom-up traversal of the tree, computing possible
    states for each subtree based on the automaton's transition rules.

    Args:
        automaton: a ranked finite tree automaton
        tree: a ranked tree structure  
    Returns:
        bool: True if the automaton accepts the tree, False otherwise
    """

    def accepts(self, automaton: ranked_Fta, tree: RankedTree) -> bool:
        """
        Check whether the automaton accepts the given tree.
        """
        root_states = self._compute_states(automaton, tree)
        return any(state.is_Final for state in root_states)

    def _compute_states(
        self,
        automaton: ranked_Fta,
        tree: RankedTree
    ) -> Set[State]:
        """
        Compute the set of states that can be assigned to the root
        of the given subtree.
        """

        # 1️⃣ Compute states for children
        children_states = [
            self._compute_states(automaton, child)
            for child in tree.children
        ]

        # 2️⃣ Match ranked rules
        possible_states = set()

        for rule in automaton.transitions:

            if rule.func != tree.ranked_symbol:
                continue

            if len(rule.input_states) != len(children_states):
                continue

            # Check if rule is compatible with children
            compatible = True
            for expected_state, child_set in zip(rule.input_states, children_states):
                if expected_state not in child_set:
                    compatible = False
                    break

            if compatible:
                possible_states.add(rule.output_state)

        return possible_states


# Example usage:

if __name__ == "__main__":
    from core.symbol import Ranked_Symbol
    from fta.rankedRule import ranked_Rule
    from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator

    # Create a simple ranked tree: f(a, b)
    f = Ranked_Symbol(name="f0", rank=2)
    a = Ranked_Symbol(name="f1", rank=0)

    root = RankedTree(symbol=f)
    child1 = RankedTree(symbol=a)
    child2 = RankedTree(symbol=a)

    root.add_child(child1)
    root.add_child(child2)

    print(root)  # Output: f(a,a)
    print("Is well formed:", root.is_well_formed())  # Output: True
    generator = RandomRankedFtaGenerator(
    n_states=3,
    n_symbols=2,
    max_rank=2,
    n_rules=8,
    seed=4512
)
    automaton = generator.generate()
    automaton.print_Fta()
    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(automaton, root):
        print("Tree accepted")
    else:
        print("Tree rejected")