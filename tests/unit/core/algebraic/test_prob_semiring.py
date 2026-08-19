import pytest

from tests.contracts.core.algebraic.prob_semiring_contracts import (
    ContractedProbabilitySemiring,
)

from TARgET.core.algebraic.stochastic_semiring import ProbabilitySemiring


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_probability_construction():
    p = ContractedProbabilitySemiring(0.3)

    assert p.value == 0.3


def test_probability_accepts_zero():
    assert ProbabilitySemiring(0.0).value == 0.0


def test_probability_accepts_one():
    assert ProbabilitySemiring(1.0).value == 1.0


def test_probability_rejects_value_above_one():
    with pytest.raises(ValueError):
        ProbabilitySemiring(1.1)


def test_probability_rejects_negative_value():
    with pytest.raises(ValueError):
        ProbabilitySemiring(-0.1)


# ---------------------------------------------------------------------------
# Zero and one
# ---------------------------------------------------------------------------

def test_zero():
    assert ProbabilitySemiring.zero().value == 0.0


def test_one():
    assert ProbabilitySemiring.one().value == 1.0


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def test_addition_with_valid_result():
    a = ProbabilitySemiring(0.3)
    b = ProbabilitySemiring(0.5)

    assert (a + b).value == pytest.approx(0.8)


def test_multiplication():
    a = ProbabilitySemiring(0.3)
    b = ProbabilitySemiring(0.5)

    assert (a * b).value == pytest.approx(0.15)


def test_addition_is_bounded_by_one():
    a = ProbabilitySemiring(0.7)
    b = ProbabilitySemiring(0.5)

    result = a + b

    assert result.value == 1.0

def test_addition_below_one():
    a = ProbabilitySemiring(0.3)
    b = ProbabilitySemiring(0.5)

    assert (a + b).value == pytest.approx(0.8)


def test_addition_exactly_one():
    a = ProbabilitySemiring(0.4)
    b = ProbabilitySemiring(0.6)

    assert (a + b).value == 1.0


# ---------------------------------------------------------------------------
# Identities
# ---------------------------------------------------------------------------

def test_zero_is_additive_identity():
    a = ProbabilitySemiring(0.3)

    assert a + ProbabilitySemiring.zero() == a


def test_one_is_multiplicative_identity():
    a = ProbabilitySemiring(0.3)

    assert a * ProbabilitySemiring.one() == a


def test_zero_is_multiplicatively_absorbing():
    a = ProbabilitySemiring(0.3)

    assert a * ProbabilitySemiring.zero() == ProbabilitySemiring.zero()


# ---------------------------------------------------------------------------
# Equality
# ---------------------------------------------------------------------------

def test_equal_probabilities():
    assert ProbabilitySemiring(0.3) == ProbabilitySemiring(0.3)


def test_different_probabilities():
    assert ProbabilitySemiring(0.3) != ProbabilitySemiring(0.5)


# ---------------------------------------------------------------------------
# Invalid operands
# ---------------------------------------------------------------------------

def test_addition_with_invalid_operand():
    with pytest.raises(TypeError):
        ProbabilitySemiring(0.3) + 0.2


def test_multiplication_with_invalid_operand():
    with pytest.raises(TypeError):
        ProbabilitySemiring(0.3) * 0.2


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------

def test_repr():
    assert repr(ProbabilitySemiring(0.3)) == "𝔓(0.3000)"


def test_str():
    assert str(ProbabilitySemiring(0.3)) == "𝔓(0.3000)"