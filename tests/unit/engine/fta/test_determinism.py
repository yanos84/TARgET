import pytest
import icontract

from tests.contracts.engine.fta.determinism_contracts import (
    ContractedDeterminism as DC,
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.state import State
#from TARgET.engine.fta.determinism.determinism import Determinism
from TARgET.engine.fta.determinism.semantics import BottomUpRankedSemantics


# ======================================================
# Helpers
# ======================================================

@pytest.fixture
def semantics():
    return BottomUpRankedSemantics()


def make_rule(symbol, inputs, output):
    return ranked_Rule(
        func=symbol,
        input_states=inputs,
        output_state=output,
    )


# ======================================================
# Empty / minimal cases
# ======================================================

def test_determinism_empty_rules(semantics):
    assert DC.check([], semantics) is True


def test_determinism_single_rule(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule = make_rule(f, [q0], q1)

    assert DC.check([rule], semantics) is True


# ======================================================
# Duplicate rules
# ======================================================

def test_determinism_duplicate_rule(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = make_rule(f, [q0], q1)
    rule2 = make_rule(f, [q0], q1)

    assert DC.check([rule1, rule2], semantics) is True


def test_determinism_many_duplicate_rules(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rules = [
        make_rule(f, [q0], q1)
        for _ in range(100)
    ]

    assert DC.check(rules, semantics) is True


# ======================================================
# Same LHS / different output
# ======================================================

def test_nondeterminism_same_lhs_different_output(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = make_rule(f, [q0], q1)
    rule2 = make_rule(f, [q0], q2)

    assert DC.check([rule1, rule2], semantics) is False


def test_nondeterminism_multiple_outputs(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rules = [
        make_rule(f, [q0], q1),
        make_rule(f, [q0], q2),
        make_rule(f, [q0], q3),
    ]

    assert DC.check(rules, semantics) is False


# ======================================================
# Different LHS
# ======================================================

def test_determinism_same_symbol_different_input(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = make_rule(f, [q0], q2)
    rule2 = make_rule(f, [q1], q2)

    assert DC.check([rule1, rule2], semantics) is True


def test_determinism_reversed_arguments(semantics):
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)

    f = Ranked_Symbol(name="f", rank=2)

    rule1 = make_rule(f, [q1, q2], q3)
    rule2 = make_rule(f, [q2, q1], q3)

    assert DC.check([rule1, rule2], semantics) is True


def test_determinism_reversed_arguments_different_outputs(semantics):
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)
    q4 = State(name="q4", is_Final=False)

    f = Ranked_Symbol(name="f", rank=2)

    rule1 = make_rule(f, [q1, q2], q3)
    rule2 = make_rule(f, [q2, q1], q4)

    assert DC.check([rule1, rule2], semantics) is True


# ======================================================
# Nullary symbols
# ======================================================

def test_determinism_nullary(semantics):
    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rule = make_rule(a, [], q0)

    assert DC.check([rule], semantics) is True


def test_determinism_multiple_identical_nullary_rules(semantics):
    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rules = [
        make_rule(a, [], q0)
        for _ in range(100)
    ]

    assert DC.check(rules, semantics) is True


def test_nondeterminism_nullary_different_outputs(semantics):
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rule1 = make_rule(a, [], q0)
    rule2 = make_rule(a, [], q1)

    assert DC.check([rule1, rule2], semantics) is False


# ======================================================
# Large deterministic example
# ======================================================

def test_determinism_many_rules(semantics):
    states = [
        State(name=f"q{i}", is_Final=False)
        for i in range(100)
    ]

    f = Ranked_Symbol(name="f", rank=1)

    rules = [
        make_rule(
            f,
            [states[i]],
            states[(i + 1) % 100],
        )
        for i in range(100)
    ]

    assert DC.check(rules, semantics) is True


# ======================================================
# State-name semantics
# ======================================================

def test_determinism_same_state_names(semantics):
    q0a = State(name="q0", is_Final=False)
    q0b = State(name="q0", is_Final=False)

    q1a = State(name="q1", is_Final=False)
    q1b = State(name="q1", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = make_rule(f, [q0a], q1a)
    rule2 = make_rule(f, [q0b], q1b)

    assert DC.check([rule1, rule2], semantics) is True


# ======================================================
# Contract violations
# ======================================================

def test_determinism_rejects_invalid_rules():
    semantics = BottomUpRankedSemantics()

    with pytest.raises(icontract.ViolationError):
        DC.check(None, semantics)


def test_determinism_rejects_invalid_semantics():
    with pytest.raises(icontract.ViolationError):
        DC.check([], None)

def test_determinism_empty_transitions():
    semantics = BottomUpRankedSemantics()

    result = DC.check([], semantics)

    assert result is True

def test_determinism_empty_fta():
    q0 = State(name="q0", is_Final=False)
    a = Ranked_Symbol(name="a", rank=0)
    from TARgET.core.fta.rankedfta import ranked_Fta

    fta = ranked_Fta(
        fta_name="empty",
        alphabet=[a],
        fta_states=[q0],
        transitions=[]
    )

    semantics = BottomUpRankedSemantics()

    assert DC.check(
        fta.transitions,
        semantics
    ) is True


def test_determinism_multiple_outputs_for_same_transition():
    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)

    a = Ranked_Symbol("a", rank=0)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(a, [], q1),
    ]

    semantics = BottomUpRankedSemantics()

    assert DC.check(
        rules,
        semantics
    ) is False