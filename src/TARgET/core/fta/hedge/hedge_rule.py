class HedgeTransition:
    """
    Represents a hedge automaton transition:

        symbol(horizontal_language) -> target_state

    Example:

        a(q1 q2*) -> q0
    """

    def __init__(self, symbol, horizontal_language, target_state):
        self.symbol = symbol
        self.horizontal_language = horizontal_language
        self.target_state = target_state


    def get_rule_as_str(self):
        return (
            self.symbol.name
            + "("
            + str(self.horizontal_language)
            + ") -> "
            + self.target_state.name
        )


    def __str__(self):
        return self.get_rule_as_str()