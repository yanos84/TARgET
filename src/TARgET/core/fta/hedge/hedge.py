from abc import abstractmethod
from typing import Dict, List
from ..abst_fta import Fta
from .hedge_rule import HedgeTransition
from ..state import State
from ...base.symbol import Symbol




class HedgeAutomaton(Fta):
    """
    Abstract hedge automaton.

    Transitions have the form:

        symbol(horizontal_language) -> state

    where horizontal_language is a regular language over states.
    """


    #@abstractmethod
    def __init__(self, name, states, alphabet):

        super().__init__(name, states)

        self._alphabet = alphabet

        # list of HedgeTransition objects
        self._transitions = []


    @property
    def alphabet(self):
        return self._alphabet


    @property
    def transitions(self):
        return self._transitions


    def add_transition(self, symbol, horizontal_language, target_state):

        transition = HedgeTransition(
            symbol,
            horizontal_language,
            target_state
        )

        self._transitions.append(transition)


    def print_Fta(self):
        """
        Prints the details of the hedge automaton.
        """

        print("Hedge Automaton name: " + self.name)

        print(
            "States list: "
            +
            ' '.join(
                [
                    i.name +
                    " (is final :" +
                    str(i.is_Final) +
                    "), "
                    for i in self.fta_states
                ]
            )[:-1]
        )


        print(
            "Alphabet: "
            +
            ' '.join(
                [
                    i.name + ", "
                    for i in self.alphabet
                ]
            )[:-1]
        )


        print(
            "Rules list:\n "
            +
            ' '.join(
                [
                    rule.get_rule_as_str() + "\n"
                    for rule in self.transitions
                ]
            )
        )


    def __str__(self):

        _name = (
            "Hedge Automaton name: "
            + self.name
            + "\n"
        )


        _states = (
            "States list: "
            +
            ' '.join(
                [
                    i.name +
                    " (is final :" +
                    str(i.is_Final) +
                    "), "
                    for i in self.fta_states
                ]
            )[:-1]
            +
            "\n"
        )


        _alphabet = (
            "Alphabet: "
            +
            ' '.join(
                [
                    i.name + ", "
                    for i in self.alphabet
                ]
            )[:-1]
            +
            "\n"
        )


        _rules = (
            "Rules list:\n "
            +
            ' '.join(
                [
                    rule.get_rule_as_str() + "\n"
                    for rule in self.transitions
                ]
            )
            +
            "\n"
        )


        return _name + _states + _alphabet + _rules

if __name__ == "__main__":
# -------------------------
# Define states
# -------------------------

    q0 = State("q0", is_Final=True)
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=False)


    states = [
        q0,
        q1,
        q2
    ]


    # -------------------------
    # Define alphabet
    # -------------------------

    a = Symbol("a")
    b = Symbol("b")


    alphabet = [
        a,
        b
    ]


    # -------------------------
    # Create hedge automaton
    # -------------------------

    ha = HedgeAutomaton(
        name="Example HA",
        states=states,
        alphabet=alphabet
    )


    # -------------------------
    # Add hedge transitions
    # -------------------------

    # a(q1 q2*) -> q0
    ha.add_transition(
        symbol=a,
        horizontal_language="q1(q2)*",
        target_state=q0
    )


    # b(epsilon) -> q1
    ha.add_transition(
        symbol=b,
        horizontal_language="epsilon",
        target_state=q1
    )


    # -------------------------
    # Print automaton
    # -------------------------

    print(ha)