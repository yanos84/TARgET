import pytest

from tests.contracts.core.fta.rule_contracts import (
    ContractedRankedRule,
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.state import State


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def nullary_symbol():
    return Ranked_Symbol("a", 0)


@pytest.fixture
def unary_symbol():
    return Ranked_Symbol("f", 1)


@pytest.fixture
def binary_symbol():
    return Ranked_Symbol("g", 2)


@pytest.fixture
def states():
    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=False)
    q2 = State("q2", is_Final=True)

    return q0, q1, q2


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_ranked_rule_construction(
    unary_symbol,
    states,
):
    q0, _, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert rule.func == unary_symbol
    assert rule.input_states == [q0]
    assert rule.output_state == q2
    assert rule.is_weighted is False
    assert rule.weight is None


def test_ranked_rule_default_construction():
    rule = ContractedRankedRule()

    assert rule.func is None
    assert rule.input_states is None
    assert rule.output_state is None
    assert rule.is_weighted is False
    assert rule.weight is None


# ---------------------------------------------------------------------------
# Validity
# ---------------------------------------------------------------------------

def test_nullary_rule_is_valid(
    nullary_symbol,
    states,
):
    _, _, q2 = states

    rule = ContractedRankedRule(
        func=nullary_symbol,
        input_states=[],
        output_state=q2,
    )

    assert rule.is_valid() is True


def test_unary_rule_is_valid(
    unary_symbol,
    states,
):
    q0, _, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert rule.is_valid() is True


def test_binary_rule_is_valid(
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    assert rule.is_valid() is True


# ---------------------------------------------------------------------------
# Invalid rank / input-state combinations
# ---------------------------------------------------------------------------

def test_rule_with_too_few_input_states_is_invalid(
    binary_symbol,
    states,
):
    q0, _, q2 = states

    rule = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    with pytest.raises(Exception):
        rule.is_valid()


def test_rule_with_too_many_input_states_is_invalid(
    unary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    with pytest.raises(Exception):
        rule.is_valid()


def test_rank_zero_rule_rejects_any_input_state(
    nullary_symbol,
    states,
):
    q0, _, q2 = states

    rule = ContractedRankedRule(
        func=nullary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    with pytest.raises(Exception):
        rule.is_valid()


# ---------------------------------------------------------------------------
# Input-state ordering
# ---------------------------------------------------------------------------

def test_input_state_order_is_preserved(
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    assert rule.input_states[0] == q0
    assert rule.input_states[1] == q1


def test_reordering_input_states_changes_rule(
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule1 = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    rule2 = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q1, q0],
        output_state=q2,
    )

    assert rule1 != rule2


# ---------------------------------------------------------------------------
# Equality
# ---------------------------------------------------------------------------

def test_equal_rules():
    symbol = Ranked_Symbol("f", 1)

    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)

    rule1 = ContractedRankedRule(
        func=symbol,
        input_states=[q0],
        output_state=q1,
    )

    rule2 = ContractedRankedRule(
        func=symbol,
        input_states=[q0],
        output_state=q1,
    )

    assert rule1 == rule2


def test_rules_with_different_symbols_are_not_equal(
    states,
):
    q0, _, q2 = states

    rule1 = ContractedRankedRule(
        func=Ranked_Symbol("f", 1),
        input_states=[q0],
        output_state=q2,
    )

    rule2 = ContractedRankedRule(
        func=Ranked_Symbol("g", 1),
        input_states=[q0],
        output_state=q2,
    )

    assert rule1 != rule2


def test_rules_with_different_input_states_are_not_equal(
    unary_symbol,
    states,
):
    q0, q1, q2 = states

    rule1 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    rule2 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q1],
        output_state=q2,
    )

    assert rule1 != rule2


def test_rules_with_different_output_states_are_not_equal(
    unary_symbol,
    states,
):
    q0, q1, q2 = states

    rule1 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q1,
    )

    rule2 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert rule1 != rule2


def test_rule_not_equal_to_other_types(
    unary_symbol,
    states,
):
    q0, _, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert rule != None
    assert rule != "rule"
    assert rule != 1
    assert rule != []


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def test_equal_rules_have_same_hash(
    unary_symbol,
    states,
):
    q0, _, q2 = states

    rule1 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    rule2 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert rule1 == rule2
    assert hash(rule1) == hash(rule2)


def test_equal_rules_are_deduplicated_in_set(
    unary_symbol,
    states,
):
    q0, _, q2 = states

    rule1 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    rule2 = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert len({rule1, rule2}) == 1


def test_different_rules_can_coexist_in_set(
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule1 = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    rule2 = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q1, q0],
        output_state=q2,
    )

    assert len({rule1, rule2}) == 2


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------

def test_nullary_rule_string(
    nullary_symbol,
    states,
):
    _, _, q2 = states

    rule = ContractedRankedRule(
        func=nullary_symbol,
        input_states=[],
        output_state=q2,
    )

    assert str(rule) == "a()---->q2"


def test_unary_rule_string(
    unary_symbol,
    states,
):
    q0, _, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    assert str(rule) == "f(q0)---->q2"


def test_binary_rule_string(
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    assert str(rule) == "g(q0, q1)---->q2"


def test_get_rule_as_str_matches_str(
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=binary_symbol,
        input_states=[q0, q1],
        output_state=q2,
    )

    assert rule.get_rule_as_str() == str(rule)


# ---------------------------------------------------------------------------
# Attribute manipulation
# ---------------------------------------------------------------------------

def test_rule_function_can_be_modified(
    unary_symbol,
    binary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    rule.func = binary_symbol

    assert rule.func == binary_symbol


def test_rule_input_states_can_be_modified(
    unary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q2,
    )

    rule.input_states = [q1]

    assert rule.input_states == [q1]


def test_rule_output_state_can_be_modified(
    unary_symbol,
    states,
):
    q0, q1, q2 = states

    rule = ContractedRankedRule(
        func=unary_symbol,
        input_states=[q0],
        output_state=q1,
    )

    rule.output_state = q2

    assert rule.output_state == q2