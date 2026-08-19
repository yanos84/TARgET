import pytest

from tests.contracts.core.fta.fta_contracts import (
    ContractedRankedFta,
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.state import State


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def states():
    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)
    q2 = State("q2", is_Final=True)

    return q0, q1, q2


@pytest.fixture
def alphabet():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 1)

    return [a, f]


@pytest.fixture
def transitions(states, alphabet):
    q0, q1, _ = states
    a, f = alphabet

    return [
        ranked_Rule(
            func=a,
            input_states=[],
            output_state=q0,
        ),
        ranked_Rule(
            func=f,
            input_states=[q0],
            output_state=q1,
        ),
    ]


@pytest.fixture
def fta(states, alphabet, transitions):
    return ContractedRankedFta(
        fta_name="test_fta",
        alphabet=alphabet,
        fta_states=list(states),
        transitions=transitions,
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_fta_construction(fta, states, alphabet, transitions):
    assert fta.name == "test_fta"
    assert fta.fta_states == list(states)
    assert fta.alphabet == alphabet
    assert fta.transitions == transitions


def test_fta_default_name():
    fta = ContractedRankedFta()

    assert fta.name == "default_fta"


def test_fta_empty_construction():
    fta = ContractedRankedFta(
        fta_name="empty",
        alphabet=[],
        fta_states=[],
        transitions=[],
    )

    assert fta.name == "empty"
    assert fta.fta_states == []
    assert fta.alphabet == []
    assert fta.transitions == []


# ---------------------------------------------------------------------------
# Name
# ---------------------------------------------------------------------------

def test_fta_name_can_be_modified(fta):
    fta.name = "new_name"

    assert fta.name == "new_name"


def test_fta_name_can_be_set_to_empty_string(fta):
    fta.name = ""

    assert fta.name == ""


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def test_add_state(fta):
    new_state = State("q3", is_Final=False)

    fta.add_state(new_state)

    assert new_state in fta.fta_states
    assert len(fta.fta_states) == 4


def test_add_duplicate_state_is_rejected(fta, states):
    q0, _, _ = states

    with pytest.raises(Exception):
        fta.add_state(q0)


def test_add_duplicate_state_does_not_change_state_list(fta, states):
    q0, _, _ = states

    original_length = len(fta.fta_states)

    with pytest.raises(Exception):
        fta.add_state(q0)

    assert len(fta.fta_states) == original_length


def test_remove_state(fta, states):
    q0, _, _ = states

    fta.remove_from_states(q0)

    assert q0 not in fta.fta_states
    assert len(fta.fta_states) == 2


def test_remove_nonexistent_state_raises(fta):
    state = State("unknown", is_Final=False)

    with pytest.raises(ValueError):
        fta.remove_from_states(state)


def test_fta_states_setter(fta):
    new_states = [
        State("p0", is_Final=False),
        State("p1", is_Final=True),
    ]

    fta.fta_states = new_states

    assert fta.fta_states == new_states


def test_fta_states_empty_list(fta):
    fta.fta_states = []

    assert fta.fta_states == []


# ---------------------------------------------------------------------------
# Final states
# ---------------------------------------------------------------------------

def test_get_final_states(fta):
    assert fta.get_final_states() == {"q1", "q2"}


def test_get_final_states_empty_fta():
    fta = ContractedRankedFta(
        fta_name="empty",
        alphabet=[],
        fta_states=[],
        transitions=[],
    )

    assert fta.get_final_states() == set()


def test_get_final_states_when_no_state_is_final():
    states = [
        State("q0", is_Final=False),
        State("q1", is_Final=False),
    ]

    fta = ContractedRankedFta(
        fta_name="no_final",
        alphabet=[],
        fta_states=states,
        transitions=[],
    )

    assert fta.get_final_states() == set()


def test_get_final_states_returns_state_names(fta):
    result = fta.get_final_states()

    assert result == {"q1", "q2"}
    assert all(isinstance(state_name, str) for state_name in result)


# ---------------------------------------------------------------------------
# Alphabet
# ---------------------------------------------------------------------------

def test_fta_alphabet(fta, alphabet):
    assert fta.alphabet == alphabet


def test_fta_empty_alphabet():
    fta = ContractedRankedFta(
        fta_name="no_alphabet",
        alphabet=[],
        fta_states=[],
        transitions=[],
    )

    assert fta.alphabet == []


def test_alphabet_contains_ranked_symbols(fta):
    assert all(
        isinstance(symbol, Ranked_Symbol)
        for symbol in fta.alphabet
    )


# ---------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------

def test_fta_transitions(fta, transitions):
    assert fta.transitions == transitions


def test_fta_empty_transitions():
    fta = ContractedRankedFta(
        fta_name="no_transitions",
        alphabet=[],
        fta_states=[],
        transitions=[],
    )

    assert fta.transitions == []


def test_fta_can_contain_multiple_equal_transitions(
    states,
    alphabet,
):
    q0, q1, _ = states
    _, f = alphabet

    rule1 = ranked_Rule(
        func=f,
        input_states=[q0],
        output_state=q1,
    )

    rule2 = ranked_Rule(
        func=f,
        input_states=[q0],
        output_state=q1,
    )

    fta = ContractedRankedFta(
        fta_name="duplicate_rules",
        alphabet=alphabet,
        fta_states=list(states),
        transitions=[rule1, rule2],
    )

    assert len(fta.transitions) == 2
    assert rule1 == rule2


# ---------------------------------------------------------------------------
# Unweighted FTA
# ---------------------------------------------------------------------------

def test_unweighted_fta_is_not_weighted(fta):
    assert fta.chech_weighted() is False


def test_empty_fta_is_not_weighted():
    fta = ContractedRankedFta(
        fta_name="empty",
        alphabet=[],
        fta_states=[],
        transitions=[],
    )

    assert fta.chech_weighted() is False


def test_get_semiring_rejects_unweighted_fta(fta):
    with pytest.raises(ValueError):
        fta.get_semiring()


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------

def test_fta_string_contains_name(fta):
    result = str(fta)

    assert "Fta name: test_fta" in result


def test_fta_string_contains_states(fta):
    result = str(fta)

    assert "q0" in result
    assert "q1" in result
    assert "q2" in result


def test_fta_string_contains_alphabet(fta):
    result = str(fta)

    assert "a(rank = 0)" in result
    assert "f(rank = 1)" in result


def test_fta_string_contains_transitions(fta):
    result = str(fta)

    assert "a()---->q0" in result
    assert "f(q0)---->q1" in result


# ---------------------------------------------------------------------------
# print_Fta
# ---------------------------------------------------------------------------

def test_print_fta(capsys, fta):
    fta.print_Fta()

    captured = capsys.readouterr()

    assert "Fta name: test_fta" in captured.out
    assert "q0" in captured.out
    assert "q1" in captured.out
    assert "q2" in captured.out
    assert "a(rank = 0)" in captured.out
    assert "f(rank = 1)" in captured.out
    assert "a()---->q0" in captured.out
    assert "f(q0)---->q1" in captured.out