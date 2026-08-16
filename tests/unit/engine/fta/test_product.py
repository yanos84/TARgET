import pytest
import icontract

from tests.contracts.engine.fta.product_contracts import (
    ContractedRankedProd as RP
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


# ======================================================
# Test 1
# Different ground symbols
#
# FTA1:
#   a() -> q1
#   f(q1) -> qf1
#
# FTA2:
#   b() -> p1
#   f(p1) -> pf2
#
# The product construction produces the f transition,
# but it is unreachable because there is no common
# ground symbol producing (q1,p1).
# ======================================================

@pytest.fixture
def create_different_symbols_fta():

    # ---------- FTA 1 ----------

    q1 = State(name="q1", is_Final=False)
    qf1 = State(name="qf1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=1)

    rules1 = [
        ranked_Rule(a, [], q1),
        ranked_Rule(f, [q1], qf1)
    ]

    fta1 = ranked_Fta(
        fta_name="different_symbols_1",
        alphabet=[a, f],
        fta_states=[q1, qf1],
        transitions=rules1
    )

    # ---------- FTA 2 ----------

    p1 = State(name="p1", is_Final=False)
    pf2 = State(name="pf2", is_Final=True)

    b = Ranked_Symbol(name="b", rank=0)
    f2 = Ranked_Symbol(name="f", rank=1)

    rules2 = [
        ranked_Rule(b, [], p1),
        ranked_Rule(f2, [p1], pf2)
    ]

    fta2 = ranked_Fta(
        fta_name="different_symbols_2",
        alphabet=[b, f2],
        fta_states=[p1, pf2],
        transitions=rules2
    )

    return fta1, fta2


def test_product_different_symbols(create_different_symbols_fta):

    fta1, fta2 = create_different_symbols_fta

    product_computer = RP()

    product = product_computer.product(fta1, fta2)

    assert len(product.fta_states) == 2
    assert len(product.transitions) == 1

    assert product.transitions[0].func.name == "f"

    assert product.transitions[0].output_state.is_Final is True


# ======================================================
# Test 2
# Multiple nullary transitions
#
# FTA1:
#   a() -> q1
#   a() -> q2
#
# FTA2:
#   a() -> p1
#   a() -> p2
#
# Expected:
#   4 product transitions
# ======================================================

@pytest.fixture
def create_multiple_nullary_fta():

    # ---------- FTA 1 ----------

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    a1 = Ranked_Symbol(name="a", rank=0)

    rules1 = [
        ranked_Rule(a1, [], q1),
        ranked_Rule(a1, [], q2)
    ]

    fta1 = ranked_Fta(
        fta_name="multiple_nullary_1",
        alphabet=[a1],
        fta_states=[q1, q2],
        transitions=rules1
    )

    # ---------- FTA 2 ----------

    p1 = State(name="p1", is_Final=False)
    p2 = State(name="p2", is_Final=False)

    a2 = Ranked_Symbol(name="a", rank=0)

    rules2 = [
        ranked_Rule(a2, [], p1),
        ranked_Rule(a2, [], p2)
    ]

    fta2 = ranked_Fta(
        fta_name="multiple_nullary_2",
        alphabet=[a2],
        fta_states=[p1, p2],
        transitions=rules2
    )

    return fta1, fta2


def test_product_multiple_nullary_transitions(
    create_multiple_nullary_fta
):

    fta1, fta2 = create_multiple_nullary_fta

    product_computer = RP()

    product = product_computer.product(fta1, fta2)

    assert len(product.transitions) == 4
    assert len(product.fta_states) == 4

    expected_states = {
        "(q1,p1)",
        "(q1,p2)",
        "(q2,p1)",
        "(q2,p2)"
    }

    actual_states = {
        state.name
        for state in product.fta_states
    }

    assert actual_states == expected_states


# ======================================================
# Test 3
# Binary combinations
#
# FTA1:
#   a() -> q1
#   a() -> q2
#   f(q1,q2) -> qf
#   f(q2,q1) -> qf
#
# FTA2:
#   a() -> p1
#   a() -> p2
#   f(p1,p2) -> pf
#   f(p2,p1) -> pf
#
# Expected:
#   4 a transitions
#   4 f transitions
#   8 transitions total
#   5 states
# ======================================================

@pytest.fixture
def create_binary_fta():

    # ---------- FTA 1 ----------

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a1 = Ranked_Symbol(name="a", rank=0)
    f1 = Ranked_Symbol(name="f", rank=2)

    rules1 = [
        ranked_Rule(a1, [], q1),
        ranked_Rule(a1, [], q2),
        ranked_Rule(f1, [q1, q2], qf),
        ranked_Rule(f1, [q2, q1], qf)
    ]

    fta1 = ranked_Fta(
        fta_name="binary_1",
        alphabet=[a1, f1],
        fta_states=[q1, q2, qf],
        transitions=rules1
    )

    # ---------- FTA 2 ----------

    p1 = State(name="p1", is_Final=False)
    p2 = State(name="p2", is_Final=False)
    pf = State(name="pf", is_Final=True)

    a2 = Ranked_Symbol(name="a", rank=0)
    f2 = Ranked_Symbol(name="f", rank=2)

    rules2 = [
        ranked_Rule(a2, [], p1),
        ranked_Rule(a2, [], p2),
        ranked_Rule(f2, [p1, p2], pf),
        ranked_Rule(f2, [p2, p1], pf)
    ]

    fta2 = ranked_Fta(
        fta_name="binary_2",
        alphabet=[a2, f2],
        fta_states=[p1, p2, pf],
        transitions=rules2
    )

    return fta1, fta2


def test_product_binary_combinations(create_binary_fta):

    fta1, fta2 = create_binary_fta

    product_computer = RP()

    product = product_computer.product(fta1, fta2)

    assert len(product.fta_states) == 5
    assert len(product.transitions) == 8

    a_transitions = [
        rule
        for rule in product.transitions
        if rule.func.name == "a"
    ]

    f_transitions = [
        rule
        for rule in product.transitions
        if rule.func.name == "f"
    ]

    assert len(a_transitions) == 4
    assert len(f_transitions) == 4

    assert all(
        rule.output_state.is_Final
        for rule in f_transitions
    )


# ======================================================
# Test 4
# Same symbol name but different rank
#
# FTA1:
#   f has rank 1
#
# FTA2:
#   f has rank 2
#
# Expected:
#   f transitions must NOT be combined.
# ======================================================

@pytest.fixture
def create_different_rank_fta():

    # ---------- FTA 1 ----------

    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a1 = Ranked_Symbol(name="a", rank=0)
    f1 = Ranked_Symbol(name="f", rank=1)

    rules1 = [
        ranked_Rule(a1, [], q1),
        ranked_Rule(f1, [q1], qf)
    ]

    fta1 = ranked_Fta(
        fta_name="different_rank_1",
        alphabet=[a1, f1],
        fta_states=[q1, qf],
        transitions=rules1
    )

    # ---------- FTA 2 ----------

    p1 = State(name="p1", is_Final=False)
    pf = State(name="pf", is_Final=True)

    a2 = Ranked_Symbol(name="a", rank=0)
    f2 = Ranked_Symbol(name="f", rank=2)

    rules2 = [
        ranked_Rule(a2, [], p1),
        ranked_Rule(f2, [p1, p1], pf)
    ]

    fta2 = ranked_Fta(
        fta_name="different_rank_2",
        alphabet=[a2, f2],
        fta_states=[p1, pf],
        transitions=rules2
    )

    return fta1, fta2


def test_product_different_rank(create_different_rank_fta):

    fta1, fta2 = create_different_rank_fta

    product_computer = RP()

    product = product_computer.product(fta1, fta2)

    assert len(product.transitions) == 1

    assert product.transitions[0].func.name == "a"


# ======================================================
# Test 5
# Final-state mismatch
#
# qf is final.
# p1 is not final.
#
# Therefore (qf,p1) must not be final.
# ======================================================

@pytest.fixture
def create_final_state_mismatch_fta():

    qf = State(name="qf", is_Final=True)
    p1 = State(name="p1", is_Final=False)

    a1 = Ranked_Symbol(name="a", rank=0)
    a2 = Ranked_Symbol(name="a", rank=0)

    rules1 = [
        ranked_Rule(a1, [], qf)
    ]

    rules2 = [
        ranked_Rule(a2, [], p1)
    ]

    fta1 = ranked_Fta(
        fta_name="final_mismatch_1",
        alphabet=[a1],
        fta_states=[qf],
        transitions=rules1
    )

    fta2 = ranked_Fta(
        fta_name="final_mismatch_2",
        alphabet=[a2],
        fta_states=[p1],
        transitions=rules2
    )

    return fta1, fta2


def test_product_final_state_mismatch(
    create_final_state_mismatch_fta
):

    fta1, fta2 = create_final_state_mismatch_fta

    product_computer = RP()

    product = product_computer.product(fta1, fta2)

    assert len(product.transitions) == 1
    assert len(product.fta_states) == 1

    product_state = product.fta_states[0]

    assert product_state.name == "(qf,p1)"
    assert product_state.is_Final is False


# ======================================================
# Test 6
# Duplicate product states
#
# a() -> q
# b() -> q
#
# a() -> p
# b() -> p
#
# Expected:
#   only one (q,p) state.
# ======================================================

@pytest.fixture
def create_duplicate_state_fta():

    # ---------- FTA 1 ----------

    q = State(name="q", is_Final=False)

    a1 = Ranked_Symbol(name="a", rank=0)
    b1 = Ranked_Symbol(name="b", rank=0)

    rules1 = [
        ranked_Rule(a1, [], q),
        ranked_Rule(b1, [], q)
    ]

    fta1 = ranked_Fta(
        fta_name="duplicate_states_1",
        alphabet=[a1, b1],
        fta_states=[q],
        transitions=rules1
    )

    # ---------- FTA 2 ----------

    p = State(name="p", is_Final=False)

    a2 = Ranked_Symbol(name="a", rank=0)
    b2 = Ranked_Symbol(name="b", rank=0)

    rules2 = [
        ranked_Rule(a2, [], p),
        ranked_Rule(b2, [], p)
    ]

    fta2 = ranked_Fta(
        fta_name="duplicate_states_2",
        alphabet=[a2, b2],
        fta_states=[p],
        transitions=rules2
    )

    return fta1, fta2


def test_product_duplicate_states(create_duplicate_state_fta):

    fta1, fta2 = create_duplicate_state_fta

    product_computer = RP()

    product = product_computer.product(fta1, fta2)

    assert len(product.fta_states) == 1
    assert len(product.transitions) == 2

    assert product.fta_states[0].name == "(q,p)"


# ======================================================
# Contract tests
# ======================================================

def test_product_rejects_invalid_first_fta():

    product_computer = RP()

    with pytest.raises(icontract.ViolationError):
        product_computer.product(None, None)


def test_product_rejects_invalid_second_fta():

    fta1, _ = create_different_symbols_fta.__wrapped__()

    product_computer = RP()

    with pytest.raises(icontract.ViolationError):
        product_computer.product(fta1, None)