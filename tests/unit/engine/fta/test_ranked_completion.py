import pytest
import icontract

from tests.contracts.engine.fta.ranked_completion_contracts import (
    ContractedRankedCompletion as CC
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


def print_transitions(fta):
    for rule in fta.transitions:
        inputs = ", ".join(
            state.name for state in rule.input_states
        )

        print(
            f"{rule.func.name}({inputs}) "
            f"-> {rule.output_state.name}"
        )


def test_completion_empty_fta():

    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    automaton = ranked_Fta(
        fta_name="empty_fta",
        alphabet=[a, g],
        fta_states=[q0],
        transitions=[]
    )

    completion = CC(automaton)
    completed = completion.compute_completion()

    print("\nEmpty FTA:")
    print_transitions(completed)


def test_completion_nondeterministic_fta():

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    rules = [
        # a() -> q0
        ranked_Rule(a, [], q0),

        # a() -> q1
        ranked_Rule(a, [], q1),
    ]

    automaton = ranked_Fta(
        fta_name="nondeterministic_fta",
        alphabet=[a, g],
        fta_states=[q0, q1],
        transitions=rules
    )

    completion = CC(automaton)
    completed = completion.compute_completion()

    print("\nNondeterministic FTA:")
    print_transitions(completed)


def test_completion_binary_symbol():

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    h = Ranked_Symbol(name="h", rank=2)

    rules = [
        # a() -> q0
        ranked_Rule(a, [], q0),

        # h(q0, q0) -> q1
        ranked_Rule(h, [q0, q0], q1),
    ]

    automaton = ranked_Fta(
        fta_name="binary_fta",
        alphabet=[a, h],
        fta_states=[q0, q1],
        transitions=rules
    )

    completion = CC(automaton)
    completed = completion.compute_completion()

    print("\nBinary-symbol FTA:")
    print_transitions(completed)


def test_completion_rejects_invalid_fta():

    completion = CC(None)

    with pytest.raises(icontract.ViolationError):
        completion.compute_completion()