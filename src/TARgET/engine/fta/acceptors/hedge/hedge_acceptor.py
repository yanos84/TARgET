import re


class HedgeAcceptor:
    """
    Bottom-up recognizer for hedge automata.

    The acceptance algorithm:
    - recursively computes possible states for each subtree
    - builds the horizontal word of child states
    - checks if the word belongs to a horizontal language
    - returns the possible states of the current node
    """

    def __init__(self, hedge_automaton):
        self.automaton = hedge_automaton


    def accepts(self, tree):
        """
        Returns True if the tree is accepted by the hedge automaton.
        """

        states = self._recognize(tree)

        final_states = self.automaton.get_final_states()

        return any(
            state.name in final_states
            for state in states
        )


    def _recognize(self, node):
        """
        Computes the set of states reachable from a tree node.
        """

        # Compute possible states of children
        child_states = [
            self._recognize(child)
            for child in node.children
        ]


        possible_states = set()


        # Try every possible horizontal combination
        for sequence in self._horizontal_sequences(child_states):

            for transition in self.automaton.transitions:

                # IMPORTANT:
                # Tree symbols are strings,
                # automaton symbols are Symbol objects
                if transition.symbol.name == node.symbol:

                    if self._matches_horizontal_language(
                        sequence,
                        transition.horizontal_language
                    ):
                        possible_states.add(
                            transition.target_state
                        )

        return possible_states



    def _horizontal_sequences(self, child_states):
        """
        Generates all possible sequences of child states.

        Example:
            [{q1}, {q2,q3}]

        gives:
            [q1,q2]
            [q1,q3]
        """

        if not child_states:
            yield []
            return


        first = child_states[0]
        rest = child_states[1:]


        for state in first:
            for suffix in self._horizontal_sequences(rest):
                yield [state] + suffix



    def _matches_horizontal_language(self, sequence, regex):
        """
        Checks if a sequence of states belongs to a horizontal language.

        Example:
            [q1,q2,q2]

        becomes:

            q1q2q2

        and is tested against:

            q1(q2)*
        """

        word = ''.join(
            state.name
            for state in sequence
        )


        return re.fullmatch(
            regex,
            word
        ) is not None

    #example usage

if __name__ == "__main__":
    from TARgET.core.fta.state import State
    from TARgET.core.base.symbol import Symbol
    from TARgET.core.fta.hedge.hedge import HedgeAutomaton
    from TARgET.core.base.unrankedTree import UnrankedTree


    q0 = State("q0", True)
    q1 = State("q1", False)
    q2 = State("q2", False)

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")

    ha = HedgeAutomaton("HA example",[q0,q1,q2],[a,b,c])
    ha.add_transition(a,r"q1(q2)*",q0)
    ha.add_transition(b,r"",q1)
    ha.add_transition(c,r"",q2)
    print(ha)

    root = UnrankedTree("a")
    root.add_child(UnrankedTree("b"))
    root.add_child(UnrankedTree("c"))
    root.add_child(UnrankedTree("c"))

    acceptor = HedgeAcceptor(ha)

    print(acceptor.accepts(root))