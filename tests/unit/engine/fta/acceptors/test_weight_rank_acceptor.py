import pytest
import icontract

from tests.contracts.engine.fta.weighted_accept_contracts import (
    ContractedWeightedRankedBottomUpAcceptor as WRBA,
)

from TARgET.core.algebraic.stochastic_semiring import ProbabilitySemiring
from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


# ======================================================
# Fixtures
# ======================================================

@pytest.fixture
def weighted_nullary():
    """
    a() -> qf [0.5]
    qf final.
    """
    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(
            a,
            [],
            qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.5),
        )
    ]

    automaton = ranked_Fta(
        fta_name="weighted_nullary",
        alphabet=[a],
        fta_states=[qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def weighted_binary():
    """
    a()      -> q0 [0.2]
    b()      -> q1 [0.3]
    f(q0,q1) -> qf [0.5]

    Expected weight: 0.03
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
        ranked_Rule(
            a,
            [],
            q0,
            is_weighted=True,
            weight=ProbabilitySemiring(0.2),
        ),
        ranked_Rule(
            b,
            [],
            q1,
            is_weighted=True,
            weight=ProbabilitySemiring(0.3),
        ),
        ranked_Rule(
            f,
            [q0, q1],
            qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.5),
        ),
    ]

    automaton = ranked_Fta(
        fta_name="weighted_binary",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def weighted_multiple_rules():
    """
    a() -> qf [0.2]
    a() -> qf [0.3]

    Expected weight: 0.5
    """
    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(
            a,
            [],
            qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.2),
        ),
        ranked_Rule(
            a,
            [],
            qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.3),
        ),
    ]

    automaton = ranked_Fta(
        fta_name="weighted_multiple_rules",
        alphabet=[a],
        fta_states=[qf],
        transitions=rules,
    )

    return automaton, tree


@pytest.fixture
def weighted_multiple_final_states():
    """
    a() -> q1 [0.2]
    a() -> q2 [0.3]

    Both states are final.

    Expected total: 0.5
    """
    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    q1 = State(name="q1", is_Final=True)
    q2 = State(name="q2", is_Final=True)

    rules = [
        ranked_Rule(
            a,
            [],
            q1,
            is_weighted=True,
            weight=ProbabilitySemiring(0.2),
        ),
        ranked_Rule(
            a,
            [],
            q2,
            is_weighted=True,
            weight=ProbabilitySemiring(0.3),
        ),
    ]

    automaton = ranked_Fta(
        fta_name="weighted_multiple_final",
        alphabet=[a],
        fta_states=[q1, q2],
        transitions=rules,
    )

    return automaton, tree


# ======================================================
# Acceptance tests
# ======================================================

def test_weighted_nullary(weighted_nullary):
    automaton, tree = weighted_nullary

    acceptor = WRBA()

    result = acceptor.accepts(automaton, tree)

    assert result.value == pytest.approx(0.5)


def test_weighted_binary(weighted_binary):
    automaton, tree = weighted_binary

    acceptor = WRBA()

    result = acceptor.accepts(automaton, tree)

    assert result.value == pytest.approx(0.03)


def test_weighted_multiple_rules(weighted_multiple_rules):
    automaton, tree = weighted_multiple_rules

    acceptor = WRBA()

    result = acceptor.accepts(automaton, tree)

    assert result.value == pytest.approx(0.5)


def test_weighted_multiple_final_states(weighted_multiple_final_states):
    automaton, tree = weighted_multiple_final_states

    acceptor = WRBA()

    result = acceptor.accepts(automaton, tree)

    assert result.value == pytest.approx(0.5)


# ======================================================
# Contract tests
# ======================================================

def test_weighted_acceptor_rejects_invalid_automaton():
    acceptor = WRBA()

    a = Ranked_Symbol(name="a", rank=0)
    tree = RankedTree(symbol=a)

    with pytest.raises(icontract.ViolationError):
        acceptor.accepts(None, tree)


def test_weighted_acceptor_rejects_invalid_tree():
    acceptor = WRBA()

    a = Ranked_Symbol(name="a", rank=0)

    qf = State(name="qf", is_Final=True)

    rule = ranked_Rule(
        a,
        [],
        qf,
        is_weighted=True,
        weight=ProbabilitySemiring(0.5),
    )

    automaton = ranked_Fta(
        fta_name="invalid_tree",
        alphabet=[a],
        fta_states=[qf],
        transitions=[rule],
    )

    with pytest.raises(icontract.ViolationError):
        acceptor.accepts(automaton, None)