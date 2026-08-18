from itertools import product
import copy

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule


class Completion:
    """
    Complete a finite tree automaton.

    For every symbol f of rank k and every k-tuple of states,
    at least one transition f(q1, ..., qk) -> q must exist.

    Existing transitions are preserved. Missing transitions
    are directed to a non-final sink state.
    """

    def __init__(self, fta):
        self.fta = copy.deepcopy(fta)

    def compute_completion(self):
        states = self.fta.fta_states
        alphabet = self.fta.alphabet
        transitions = self.fta.transitions

        # Create sink state.
        sink = State(name="sink", is_Final=False)

        # Avoid collision with an existing state name.
        if any(state.name == "sink" for state in states):
            raise ValueError(
                "FTA already contains a state named 'sink'."
            )

        states.append(sink)

        # The sink is part of the completed state set.
        all_states = list(states)

        for symbol in alphabet:
            rank = symbol.rank

            for input_states in product(all_states, repeat=rank):

                # Does at least one transition exist for this
                # symbol and this tuple of input states?
                exists = any(
                    rule.func == symbol
                    and rule.input_states == list(input_states)
                    for rule in transitions
                )

                if not exists:
                    rule = ranked_Rule(func=symbol)
                    rule.input_states = list(input_states)
                    rule.output_state = sink
                    transitions.append(rule)

        return self.fta

#______example of usagae

#____example 1______ Simple of Complement of an FTA

def simple_example():
    # States
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=True)

    # Alphabet
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    # a() -> q0
    rule_a = ranked_Rule(func=a)
    rule_a.input_states = []
    rule_a.output_state = q0

    # g(q0) -> q1
    rule_g = ranked_Rule(func=g)
    rule_g.input_states = [q0]
    rule_g.output_state = q1

    # Original FTA
    fta = ranked_Fta(
        fta_name="example",
        fta_states=[q0, q1],
        alphabet=[a, b, g],
        transitions=[rule_a, rule_g],
    )

    print("Original FTA:")
    print(fta)
    completor = Completion(fta=fta).compute_completion()
    #completed_fta = completor.compute_completion()
    print("Completed FTA:")
    print(completor)

#______example 2________Completion with empty fta

def test_completion_empty_fta():
    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    fta = ranked_Fta(
        fta_name="empty",
        fta_states=[q0],
        alphabet=[a, g],
        transitions=[],
    )

    completed = Completion(fta).compute_completion()

    print("\nEmpty FTA completion:")
    for rule in completed.transitions:
        print(
            f"{rule.func.name}"
            f"({', '.join(s.name for s in rule.input_states)})"
            f" -> {rule.output_state.name}"
        )

#_____example 3________Completion with non deterministic fta

def test_completion_nondeterministic_fta():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    # a() -> q0
    rule_a0 = ranked_Rule(func=a)
    rule_a0.input_states = []
    rule_a0.output_state = q0

    # a() -> q1
    rule_a1 = ranked_Rule(func=a)
    rule_a1.input_states = []
    rule_a1.output_state = q1

    fta = ranked_Fta(
        fta_name="nondeterministic",
        fta_states=[q0, q1],
        alphabet=[a, g],
        transitions=[rule_a0, rule_a1],
    )

    completed = Completion(fta).compute_completion()

    print("\nNondeterministic FTA completion:")
    for rule in completed.transitions:
        print(
            f"{rule.func.name}"
            f"({', '.join(s.name for s in rule.input_states)})"
            f" -> {rule.output_state.name}"
        )

#______example-4_____binary symbol completion example

def test_completion_binary_symbol():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    h = Ranked_Symbol(name="h", rank=2)

    # a() -> q0
    rule_a = ranked_Rule(func=a)
    rule_a.input_states = []
    rule_a.output_state = q0

    # h(q0, q0) -> q1
    rule_h = ranked_Rule(func=h)
    rule_h.input_states = [q0, q0]
    rule_h.output_state = q1

    fta = ranked_Fta(
        fta_name="binary",
        fta_states=[q0, q1],
        alphabet=[a, h],
        transitions=[rule_a, rule_h],
    )

    completed = Completion(fta).compute_completion()

    print("\nBinary-symbol FTA completion:")
    for rule in completed.transitions:
        print(
            f"{rule.func.name}"
            f"({', '.join(s.name for s in rule.input_states)})"
            f" -> {rule.output_state.name}"
        )

#____example 5_____

def test_completion_empty_fta_directly():
    q0 = State("q0", is_Final=False)

    a = Ranked_Symbol("a", rank=0)

    fta = ranked_Fta(
        fta_name="empty",
        alphabet=[a],
        fta_states=[q0],
        transitions=[]
    )

    completed = Completion(fta).compute_completion()

    print("\nCompleted FTA:")
    print(completed)

if __name__ == "__main__":
    simple_example()
    test_completion_empty_fta()
    test_completion_nondeterministic_fta()
    test_completion_binary_symbol()
    test_completion_empty_fta_directly()