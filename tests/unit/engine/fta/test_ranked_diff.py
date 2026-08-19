import pytest
import icontract

from tests.contracts.engine.fta.ranked_diff_contracts import (
    ContractedRankedDiff as RD
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.engine.fta.emptiness.ranked_emptiness import RankedEmptiness


# ======================================================
# Helper
# ======================================================

def make_fta(name, states, alphabet, transitions):
    return ranked_Fta(
        fta_name=name,
        alphabet=alphabet,
        fta_states=states,
        transitions=transitions,
    )


# ======================================================
# Fixtures
# ======================================================

@pytest.fixture
def empty_fta():
    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    return make_fta(
        "empty",
        [q0],
        [a],
        [],
    )


@pytest.fixture
def accepts_a():
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)

    rules = [
        ranked_Rule(a, [], qf)
    ]

    return make_fta(
        "accepts_a",
        [qf],
        [a],
        rules,
    )


@pytest.fixture
def accepts_b():
    qf = State(name="qf", is_Final=True)

    b = Ranked_Symbol(name="b", rank=0)

    rules = [
        ranked_Rule(b, [], qf)
    ]

    return make_fta(
        "accepts_b",
        [qf],
        [b],
        rules,
    )


@pytest.fixture
def accepts_a_and_b():
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    rules = [
        ranked_Rule(a, [], qf),
        ranked_Rule(b, [], qf),
    ]

    return make_fta(
        "accepts_a_and_b",
        [qf],
        [a, b],
        rules,
    )


@pytest.fixture
def accepts_nested_a():
    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    rules = [
        # a() -> q0
        ranked_Rule(a, [], q0),

        # g(q0) -> qf
        ranked_Rule(g, [q0], qf),
    ]

    return make_fta(
        "accepts_nested_a",
        [q0, qf],
        [a, g],
        rules,
    )


# ======================================================
# Difference
# ======================================================

def test_difference_same_language(accepts_a):
    diff = RD()

    result = diff.diff(accepts_a, accepts_a)

    assert RankedEmptiness().is_empty(result) is True


def test_difference_disjoint_languages(accepts_a, accepts_b):
    diff = RD()

    result = diff.diff(accepts_a, accepts_b)

    # {a} - {b} = {a}
    assert diff.is_equivalent(result, accepts_a) is True


def test_difference_empty_first(empty_fta, accepts_a):
    diff = RD()

    result = diff.diff(empty_fta, accepts_a)

    # ∅ - {a} = ∅
    assert RankedEmptiness().is_empty(result) is True


def test_difference_empty_second(accepts_a, empty_fta):
    diff = RD()

    result = diff.diff(accepts_a, empty_fta)

    # {a} - ∅ = {a}
    assert diff.is_equivalent(result, accepts_a) is True


def test_difference_subset_language(
    accepts_a,
    accepts_a_and_b,
):
    diff = RD()

    result = diff.diff(accepts_a, accepts_a_and_b)

    # {a} - {a,b} = ∅
    assert RankedEmptiness().is_empty(result) is True


def test_difference_partial_overlap(
    accepts_a_and_b,
    accepts_a,
    accepts_b,
):
    diff = RD()

    result = diff.diff(accepts_a_and_b, accepts_a)

    # {a,b} - {a} = {b}
    assert diff.is_equivalent(result, accepts_b) is True


def test_difference_nested_tree(
    accepts_nested_a,
    empty_fta,
):
    diff = RD()

    result = diff.diff(accepts_nested_a, empty_fta)

    # L - ∅ = L
    assert diff.is_equivalent(result, accepts_nested_a) is True


# ======================================================
# Equivalence
# ======================================================

def test_equivalent_identical_automata(accepts_a):
    diff = RD()

    assert diff.is_equivalent(accepts_a, accepts_a) is True


def test_equivalent_two_empty_automata(empty_fta):
    diff = RD()

    assert diff.is_equivalent(empty_fta, empty_fta) is True


def test_non_equivalent_disjoint_automata(accepts_a, accepts_b):
    diff = RD()

    assert diff.is_equivalent(accepts_a, accepts_b) is False


def test_non_equivalent_empty_vs_non_empty(empty_fta, accepts_a):
    diff = RD()

    assert diff.is_equivalent(empty_fta, accepts_a) is False


def test_non_equivalent_strict_subset(
    accepts_a,
    accepts_a_and_b,
):
    diff = RD()

    # {a} != {a,b}
    assert diff.is_equivalent(accepts_a, accepts_a_and_b) is False


# ======================================================
# Nondeterministic input
# ======================================================

def test_difference_nondeterministic_first_fta(empty_fta):
    q0 = State(name="q0", is_Final=True)
    q1 = State(name="q1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)

    fta1 = make_fta(
        "nondeterministic",
        [q0, q1],
        [a],
        [
            # Two rules for the same nullary symbol.
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),
        ],
    )

    diff = RD()

    result = diff.diff(fta1, empty_fta)

    # L(fta1) - ∅ = L(fta1)
    assert diff.is_equivalent(result, fta1) is True


# ======================================================
# Contract violations
# ======================================================

def test_difference_rejects_invalid_first_fta(accepts_a):
    diff = RD()

    with pytest.raises(icontract.ViolationError):
        diff.diff(None, accepts_a)


def test_difference_rejects_invalid_second_fta(accepts_a):
    diff = RD()

    with pytest.raises(icontract.ViolationError):
        diff.diff(accepts_a, None)


def test_equivalence_rejects_invalid_first_fta(accepts_a):
    diff = RD()

    with pytest.raises(icontract.ViolationError):
        diff.is_equivalent(None, accepts_a)


def test_equivalence_rejects_invalid_second_fta(accepts_a):
    diff = RD()

    with pytest.raises(icontract.ViolationError):
        diff.is_equivalent(accepts_a, None)