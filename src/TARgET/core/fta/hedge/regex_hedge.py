from .hedge import HedgeAutomaton
from .hedge_rule import HedgeTransition


class RegexHedgeAutomaton(HedgeAutomaton):

    def __init__(self, name, states, alphabet):
        super().__init__(name, states, alphabet)


    def add_transition(self, symbol, regex, target_state):

        if symbol not in self._transitions:
            self._transitions[symbol] = []
        rule = {
            "regex": regex,
            "target": target_state
        }
        self._transitions[symbol].append(rule)

    def print_Fta(self):
        """
        Prints the details of the hedge automaton, including its name,
        states, alphabet, and horizontal transition rules.
        """

        print("Hedge Automaton name: " + self.name)

        print(
            "States list: " +
            ' '.join(
                [
                    i.name + " (is final :" + str(i.is_Final) + "), "
                    for i in self.fta_states
                ]
            )[:-1]
        )

        print(
            "Alphabet: " +
            ' '.join(
                [
                    i.name + ", "
                    for i in self.alphabet
                ]
            )[:-1]
        )

        print(
            "Rules list:\n " +
            ' '.join(
                [
                    self.get_rule_as_str(rule) + "\n"
                    for rule in self.transitions
                ]
            )
        )

def __str__(self):
    """
    Returns a string representation of the hedge automaton.
    """

    _name = "Hedge Automaton name: " + self.name + "\n"

    _states = (
        "States list: " +
        ' '.join(
            [
                i.name + " (is final :" + str(i.is_Final) + "), "
                for i in self.fta_states
            ]
        )[:-1]
        + "\n"
    )

    _alphabet = (
        "Alphabet: " +
        ' '.join(
            [
                i.name + ", "
                for i in self.alphabet
            ]
        )[:-1]
        + "\n"
    )

    _rules = "Rules list:\n "+ ' '.join([i.get_rule_as_str()+"\n" for i in self.transitions])

    return _name + _states + _alphabet + _rules

# example of use:

if __name__ == "__main__":
    states = ["q0", "q1", "q2"]
    alphabet = ["a", "b"]
    automaton = RegexHedgeAutomaton("my_hedge_automaton", states, alphabet)

    automaton.add_transition("a", "q1 q2*", "q3")
    automaton.add_transition("b", "q0 q1*", "q2")

    print(automaton.transitions)