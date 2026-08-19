import pytest
import icontract

from tests.contracts.engine.fta.useless_states_contracts import (
    ContractedUselessStates as US,
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


# ============================================================
# Helpers
# ============================================================

def make_rule(symbol, inputs, output):
    return ranked_Rule(
        func=symbol,
        input_states=inputs,
        output_state=output,
    )


def make_fta(name, states, alphabet, transitions):
    return ranked_Fta(
        fta_name=name,
        fta_states=states,
        alphabet=alphabet,
        transitions=transitions,
    )


# ============================================================
# Test 1
# All states are useful
#
# a() -> q1
# f(q1) -> qf
#
# Both states are reachable and productive.
# ============================================================

@pytest.fixture
def useful_fta():

    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    return make_fta(
        "useful",
        [q1, qf],
        [a, f],
        [
            make_rule(a, [], q1),
            make_rule(f, [q1], qf),
        ],
    )


def test_productive_states_all_useful(useful_fta):

    productive = US().productive_states(useful_fta)

    assert {state.name for state in productive} == {
        "q1",
        "qf",
    }


def test_reachable_states_all_useful(useful_fta):

    reachable = US().reachable_states(useful_fta)

    assert {state.name for state in reachable} == {
        "q1",
        "qf",
    }


def test_drop_useless_states_none(useful_fta):

    result = US().drop_useless_states(useful_fta)

    assert {state.name for state in result.fta_states} == {
        "q1",
        "qf",
    }

    assert len(result.transitions) == 2


# ============================================================
# Test 2
# Reachable but non-productive state
#
# a() -> q1
# f(q1) -> qf
# b() -> qu
#
# qu is reachable but cannot contribute to an accepting tree.
# ============================================================

@pytest.fixture
def reachable_nonproductive_fta():

    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)
    qu = State(name="qu", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    return make_fta(
        "reachable_nonproductive",
        [q1, qf, qu],
        [a, b, f],
        [
            make_rule(a, [], q1),
            make_rule(f, [q1], qf),
            make_rule(b, [], qu),
        ],
    )


def test_reachable_nonproductive_state(
    reachable_nonproductive_fta,
):

    checker = US()

    reachable = checker.reachable_states(
        reachable_nonproductive_fta
    )

    productive = checker.productive_states(
        reachable_nonproductive_fta
    )

    assert "qu" in {state.name for state in reachable}
    assert "qu" not in {state.name for state in productive}


def test_drop_reachable_nonproductive_state(
    reachable_nonproductive_fta,
):

    result = US().drop_useless_states(
        reachable_nonproductive_fta
    )

    assert {state.name for state in result.fta_states} == {
        "q1",
        "qf",
    }

    assert len(result.transitions) == 2


# ============================================================
# Test 3
# Productive but unreachable state
#
# qf is final, therefore productive.
# But there is no transition producing qf.
#
# Therefore qf is not reachable and must be removed.
# ============================================================

@pytest.fixture
def unreachable_final_fta():

    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)

    return make_fta(
        "unreachable_final",
        [qf],
        [a],
        [],
    )


def test_productive_but_unreachable(
    unreachable_final_fta,
):

    checker = US()

    productive = checker.productive_states(
        unreachable_final_fta
    )

    reachable = checker.reachable_states(
        unreachable_final_fta
    )

    assert "qf" in {
        state.name for state in productive
    }

    assert "qf" not in {
        state.name for state in reachable
    }


def test_drop_unreachable_final(
    unreachable_final_fta,
):

    result = US().drop_useless_states(
        unreachable_final_fta
    )

    assert result.fta_states == []
    assert result.transitions == []


# ============================================================
# Test 4
# Entirely non-productive automaton
#
# a() -> q1
# f(q1) -> q2
#
# There is no final state.
# Therefore every state is useless.
# ============================================================

@pytest.fixture
def nonproductive_fta():

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    return make_fta(
        "nonproductive",
        [q1, q2],
        [a, f],
        [
            make_rule(a, [], q1),
            make_rule(f, [q1], q2),
        ],
    )


def test_nonproductive_automaton(
    nonproductive_fta,
):

    checker = US()

    assert checker.productive_states(
        nonproductive_fta
    ) == set()

    reachable = checker.reachable_states(
        nonproductive_fta
    )

    assert {state.name for state in reachable} == {
        "q1",
        "q2",
    }


def test_drop_nonproductive_automaton(
    nonproductive_fta,
):

    result = US().drop_useless_states(
        nonproductive_fta
    )

    assert result.fta_states == []
    assert result.transitions == []


# ============================================================
# Test 5
# Useless state used as an input
#
# a() -> qu
# g(qu) -> qx
#
# Neither state can reach a final state.
# ============================================================

@pytest.fixture
def useless_chain_fta():

    qu = State(name="qu", is_Final=False)
    qx = State(name="qx", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    return make_fta(
        "useless_chain",
        [qu, qx],
        [a, g],
        [
            make_rule(a, [], qu),
            make_rule(g, [qu], qx),
        ],
    )


def test_drop_useless_chain(useless_chain_fta):

    result = US().drop_useless_states(
        useless_chain_fta
    )

    assert result.fta_states == []
    assert result.transitions == []


# ============================================================
# Test 6
# Useful chain mixed with useless chain
#
# Useful:
#   a() -> q1
#   f(q1) -> qf
#
# Useless:
#   b() -> qu
#   g(qu) -> qx
# ============================================================

@pytest.fixture
def mixed_fta():

    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    qu = State(name="qu", is_Final=False)
    qx = State(name="qx", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=1)
    g = Ranked_Symbol(name="g", rank=1)

    return make_fta(
        "mixed",
        [q1, qf, qu, qx],
        [a, b, f, g],
        [
            make_rule(a, [], q1),
            make_rule(f, [q1], qf),
            make_rule(b, [], qu),
            make_rule(g, [qu], qx),
        ],
    )


def test_drop_mixed_automaton(mixed_fta):

    result = US().drop_useless_states(mixed_fta)

    assert {state.name for state in result.fta_states} == {
        "q1",
        "qf",
    }

    assert len(result.transitions) == 2

    assert {
        rule.output_state.name
        for rule in result.transitions
    } == {
        "q1",
        "qf",
    }


# ============================================================
# Test 7
# Multiple nullary transitions
#
# a() -> q1
# a() -> q2
# f(q1) -> qf
#
# q1 is useful.
# q2 is reachable but useless.
# ============================================================

@pytest.fixture
def multiple_nullary_fta():

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    return make_fta(
        "multiple_nullary",
        [q1, q2, qf],
        [a, f],
        [
            make_rule(a, [], q1),
            make_rule(a, [], q2),
            make_rule(f, [q1], qf),
        ],
    )


def test_drop_multiple_nullary(
    multiple_nullary_fta,
):

    result = US().drop_useless_states(
        multiple_nullary_fta
    )

    assert {state.name for state in result.fta_states} == {
        "q1",
        "qf",
    }

    assert len(result.transitions) == 2


# ============================================================
# Test 8
# Useless self-loop
#
# a() -> qu
# f(qu) -> qu
#
# qu is reachable but non-productive.
# ============================================================

@pytest.fixture
def useless_loop_fta():

    qu = State(name="qu", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    return make_fta(
        "useless_loop",
        [qu],
        [a, f],
        [
            make_rule(a, [], qu),
            make_rule(f, [qu], qu),
        ],
    )


def test_drop_useless_self_loop(
    useless_loop_fta,
):

    result = US().drop_useless_states(
        useless_loop_fta
    )

    assert result.fta_states == []
    assert result.transitions == []


# ============================================================
# Test 9
# Empty FTA
# ============================================================

@pytest.fixture
def empty_fta():

    return make_fta(
        "empty",
        [],
        [],
        [],
    )


def test_empty_fta(empty_fta):

    checker = US()

    assert checker.productive_states(
        empty_fta
    ) == set()

    assert checker.reachable_states(
        empty_fta
    ) == set()


def test_drop_empty_fta(empty_fta):

    result = US().drop_useless_states(empty_fta)

    assert result.fta_states == []
    assert result.transitions == []


# ============================================================
# Test 10
# Idempotence
#
# Removing useless states twice must give the same result.
# ============================================================

def test_drop_useless_states_idempotent(mixed_fta):

    checker = US()

    result = checker.drop_useless_states(
        mixed_fta
    )

    states_after_first = {
        state.name
        for state in result.fta_states
    }

    transitions_after_first = len(
        result.transitions
    )

    result = checker.drop_useless_states(result)

    states_after_second = {
        state.name
        for state in result.fta_states
    }

    transitions_after_second = len(
        result.transitions
    )

    assert states_after_first == states_after_second
    assert transitions_after_first == transitions_after_second


# ============================================================
# Contract tests
# ============================================================

def test_productive_states_rejects_invalid_fta():

    checker = US()

    with pytest.raises(icontract.ViolationError):
        checker.productive_states(None)


def test_reachable_states_rejects_invalid_fta():

    checker = US()

    with pytest.raises(icontract.ViolationError):
        checker.reachable_states(None)


def test_drop_useless_states_rejects_invalid_fta():

    checker = US()

    with pytest.raises(icontract.ViolationError):
        checker.drop_useless_states(None)