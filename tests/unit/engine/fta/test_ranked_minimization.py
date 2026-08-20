from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
import pytest

from tests.contracts.engine.fta.minimization_contracts import (
    ContractedMinimizer
)


def test_minimize_already_minimal_fta():
    q0 = State("q0", is_Final=True)

    a = Ranked_Symbol("a", rank=0)

    rule = ranked_Rule(
        a,
        [],
        q0
    )

    fta = ranked_Fta(
        fta_name="minimal",
        alphabet=[a],
        fta_states=[q0],
        transitions=[rule]
    )

    minimized = ContractedMinimizer().minimize(fta)

    assert len(minimized.fta_states) == 1
    assert len(minimized.transitions) == 1

def test_minimize_merges_equivalent_states():
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=False)
    qf = State("qf", is_Final=True)

    a = Ranked_Symbol("a", rank=0)
    b = Ranked_Symbol("b", rank=0)
    f = Ranked_Symbol("f", rank=1)

    transitions = [
        ranked_Rule(a, [], q1),
        ranked_Rule(b, [], q2),
        ranked_Rule(f, [q1], qf),
        ranked_Rule(f, [q2], qf),
    ]

    fta = ranked_Fta(
        fta_name="merge_equivalent",
        alphabet=[a, b, f],
        fta_states=[q1, q2, qf],
        transitions=transitions
    )

    minimized = ContractedMinimizer().minimize(fta)

    assert len(minimized.fta_states) == 2


def test_minimize_does_not_merge_final_and_non_final_states():
    q0 = State("q0", is_Final=False)
    qf = State("qf", is_Final=True)

    a = Ranked_Symbol("a", rank=0)
    f = Ranked_Symbol("f", rank=1)

    transitions = [
        ranked_Rule(a, [], q0),
        ranked_Rule(f, [q0], qf),
    ]

    fta = ranked_Fta(
        fta_name="finality_distinction",
        alphabet=[a, f],
        fta_states=[q0, qf],
        transitions=transitions
    )

    minimized = ContractedMinimizer().minimize(fta)

    assert len(minimized.fta_states) == 2

def test_minimize_does_not_modify_original():
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=False)
    qf = State("qf", is_Final=True)

    a = Ranked_Symbol("a", rank=0)
    b = Ranked_Symbol("b", rank=0)
    f = Ranked_Symbol("f", rank=1)

    transitions = [
        ranked_Rule(a, [], q1),
        ranked_Rule(b, [], q2),
        ranked_Rule(f, [q1], qf),
        ranked_Rule(f, [q2], qf),
    ]

    fta = ranked_Fta(
        fta_name="original",
        alphabet=[a, b, f],
        fta_states=[q1, q2, qf],
        transitions=transitions
    )

    original_states = list(fta.fta_states)
    original_transitions = list(fta.transitions)

    minimized = ContractedMinimizer().minimize(fta)

    assert minimized is not fta
    assert fta.fta_states == original_states
    assert fta.transitions == original_transitions

def test_minimize_rejects_nondeterministic_fta():
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=True)

    a = Ranked_Symbol("a", rank=0)

    transitions = [
        ranked_Rule(a, [], q1),
        ranked_Rule(a, [], q2),
    ]

    fta = ranked_Fta(
        fta_name="nondeterministic",
        alphabet=[a],
        fta_states=[q1, q2],
        transitions=transitions
    )

    with pytest.raises(ValueError, match="deterministic"):
        ContractedMinimizer().minimize(fta)


def test_minimizd_fta_is_equivalent():
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=False)
    qf = State("qf", is_Final=True)

    a = Ranked_Symbol("a", rank=0)
    b = Ranked_Symbol("b", rank=0)
    f = Ranked_Symbol("f", rank=1)

    transitions = [
        ranked_Rule(a, [], q1),
        ranked_Rule(b, [], q2),
        ranked_Rule(f, [q1], qf),
        ranked_Rule(f, [q2], qf),
    ]

    fta = ranked_Fta(
        fta_name="merge_equivalent",
        alphabet=[a, b, f],
        fta_states=[q1, q2, qf],
        transitions=transitions
    )
    from TARgET.engine.fta.equivalence.ranked_equivalence import is_equivalent
    minimized = ContractedMinimizer().minimize(fta)
    assert is_equivalent(fta,minimized)== True