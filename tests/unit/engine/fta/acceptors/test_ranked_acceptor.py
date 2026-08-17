import pytest
import icontract

from tests.contracts.engine.fta.acceptor_contracts import (
    ContractedRankedBottomUpAcceptor as RBA,
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


# ======================================================
# Fixtures
# ======================================================

@pytest.fixture
def nullary_tree_accepted():
    """
    a()

    a() -> q1

    q1 is final.
    """
    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    q1 = State(name="q1", is_Final=True)

    rules = [
        ranked_Rule(a, [], q1)
    ]

    automaton = ranked_Fta(
        fta_name="nullary_accepted",
        alphabet=[a],
        fta_states=[q1],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def nullary_tree_non_final():
    """
    a()

    a() -> q1

    q1 is not final.
    """
    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    q1 = State(name="q1", is_Final=False)

    rules = [
        ranked_Rule(a, [], q1)
    ]

    automaton = ranked_Fta(
        fta_name="nullary_non_final",
        alphabet=[a],
        fta_states=[q1],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def nullary_tree_no_transition():
    """
    Tree:

        a()

    Automaton only contains:

        b() -> q1
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    tree = RankedTree(symbol=a)

    q1 = State(name="q1", is_Final=True)

    rules = [
        ranked_Rule(b, [], q1)
    ]

    automaton = ranked_Fta(
        fta_name="nullary_no_transition",
        alphabet=[a, b],
        fta_states=[q1],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def nullary_multiple_transitions():
    """
    a() -> q1
    a() -> q2

    q1 is not final.
    q2 is final.
    """
    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=True)

    rules = [
        ranked_Rule(a, [], q1),
        ranked_Rule(a, [], q2),
    ]

    automaton = ranked_Fta(
        fta_name="nullary_multiple_transitions",
        alphabet=[a],
        fta_states=[q1, q2],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def unary_tree_accepted():
    """
    f(a)

    a()   -> q0
    f(q0) -> qf
    """
    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))

    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(f, [q0], qf),
    ]

    automaton = ranked_Fta(
        fta_name="unary_accepted",
        alphabet=[a, f],
        fta_states=[q0, qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def unary_tree_wrong_child():
    """
    f(a)

    a()   -> q0
    f(q1) -> qf

    Therefore rejected.
    """
    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(f, [q1], qf),
    ]

    automaton = ranked_Fta(
        fta_name="unary_wrong_child",
        alphabet=[a, f],
        fta_states=[q0, q1, qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def binary_tree_accepted():
    """
    f(a,b)

    a()      -> q0
    b()      -> q1
    f(q0,q1) -> qf
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))
    tree.add_child(RankedTree(symbol=b))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(b, [], q1),
        ranked_Rule(f, [q0, q1], qf),
    ]

    automaton = ranked_Fta(
        fta_name="binary_accepted",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def binary_tree_reversed():
    """
    f(b,a)

    Automaton expects:

        f(q0,q1)

    where:

        a() -> q0
        b() -> q1

    Therefore rejected.
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=b))
    tree.add_child(RankedTree(symbol=a))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(b, [], q1),
        ranked_Rule(f, [q0, q1], qf),
    ]

    automaton = ranked_Fta(
        fta_name="binary_reversed",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def binary_tree_wrong_arity():
    """
    f(a,b)

    Automaton contains only:

        f(q0) -> qf

    Wrong arity, therefore rejected.
    """
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))
    tree.add_child(RankedTree(symbol=b))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(b, [], q1),

        # Wrong arity.
        ranked_Rule(f, [q0], qf),
    ]

    automaton = ranked_Fta(
        fta_name="binary_wrong_arity",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def nondeterministic_internal_tree():
    """
    f(a)

    a() -> q0
    a() -> q1

    f(q0) -> q2
    f(q1) -> qf

    qf is final.

    The subtree a can reach both q0 and q1.
    """
    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(a, [], q0),
        ranked_Rule(a, [], q1),
        ranked_Rule(f, [q0], q2),
        ranked_Rule(f, [q1], qf),
    ]

    automaton = ranked_Fta(
        fta_name="nondeterministic_internal",
        alphabet=[a, f],
        fta_states=[q0, q1, q2, qf],
        transitions=rules,
    )

    return automaton, tree


# ======================================================
# Acceptance tests
# ======================================================

def test_accepts_nullary_tree(nullary_tree_accepted):
    automaton, tree = nullary_tree_accepted

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is True


def test_rejects_nullary_non_final_state(nullary_tree_non_final):
    automaton, tree = nullary_tree_non_final

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is False


def test_rejects_nullary_without_transition(nullary_tree_no_transition):
    automaton, tree = nullary_tree_no_transition

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is False


def test_accepts_nullary_with_multiple_transitions(
    nullary_multiple_transitions
):
    automaton, tree = nullary_multiple_transitions

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is True


def test_accepts_unary_tree(unary_tree_accepted):
    automaton, tree = unary_tree_accepted

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is True


def test_rejects_unary_wrong_child_state(unary_tree_wrong_child):
    automaton, tree = unary_tree_wrong_child

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is False


def test_accepts_binary_tree(binary_tree_accepted):
    automaton, tree = binary_tree_accepted

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is True


def test_rejects_binary_reversed_children(binary_tree_reversed):
    automaton, tree = binary_tree_reversed

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is False


def test_rejects_binary_wrong_arity(binary_tree_wrong_arity):
    automaton, tree = binary_tree_wrong_arity

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is False


def test_accepts_nondeterministic_internal_tree(
    nondeterministic_internal_tree
):
    automaton, tree = nondeterministic_internal_tree

    acceptor = RBA()

    assert acceptor.accepts(automaton, tree) is True


# ======================================================
# Contract tests
# ======================================================

def test_accepts_rejects_invalid_automaton():
    acceptor = RBA()

    a = Ranked_Symbol(name="a", rank=0)
    tree = RankedTree(symbol=a)

    with pytest.raises(icontract.ViolationError):
        acceptor.accepts(None, tree)


def test_accepts_rejects_invalid_tree():
    acceptor = RBA()

    a = Ranked_Symbol(name="a", rank=0)

    q0 = State(name="q0", is_Final=True)

    rule = ranked_Rule(
        a,
        [],
        q0,
    )

    automaton = ranked_Fta(
        fta_name="invalid_tree_test",
        alphabet=[a],
        fta_states=[q0],
        transitions=[rule],
    )

    with pytest.raises(icontract.ViolationError):
        acceptor.accepts(automaton, None)