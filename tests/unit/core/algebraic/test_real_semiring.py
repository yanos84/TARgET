import pytest

from tests.contracts.core.algebraic.real_semiring_contracts import (
    ContractedRealSemiring,
)

from TARgET.core.algebraic.real_semiring import RealSemiring


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_real_semiring_construction():
    element = ContractedRealSemiring(3.5)

    assert element.value == 3.5


def test_real_semiring_converts_value_to_float():
    element = ContractedRealSemiring(5)

    assert element.value == 5.0


def test_real_semiring_accepts_negative_value():
    element = RealSemiring(-3.5)

    assert element.value == -3.5


# ---------------------------------------------------------------------------
# Zero and one
# ---------------------------------------------------------------------------

def test_zero():
    zero = RealSemiring.zero()

    assert zero.value == 0.0


def test_one():
    one = RealSemiring.one()

    assert one.value == 1.0


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def test_addition():
    a = RealSemiring(3.5)
    b = RealSemiring(2.5)

    assert a + b == RealSemiring(6.0)


def test_multiplication():
    a = RealSemiring(3.5)
    b = RealSemiring(2.5)

    assert a * b == RealSemiring(8.75)


# ---------------------------------------------------------------------------
# Identities
# ---------------------------------------------------------------------------

def test_zero_is_additive_identity():
    a = RealSemiring(3.5)
    zero = RealSemiring.zero()

    assert a + zero == a
    assert zero + a == a


def test_one_is_multiplicative_identity():
    a = RealSemiring(3.5)
    one = RealSemiring.one()

    assert a * one == a
    assert one * a == a


def test_zero_is_multiplicatively_absorbing():
    a = RealSemiring(3.5)
    zero = RealSemiring.zero()

    assert a * zero == zero
    assert zero * a == zero


# ---------------------------------------------------------------------------
# Equality and hashing
# ---------------------------------------------------------------------------

def test_equal_real_elements():
    assert RealSemiring(3.5) == RealSemiring(3.5)


def test_different_real_elements():
    assert RealSemiring(3.5) != RealSemiring(4.5)


def test_equal_real_elements_have_same_hash():
    a = RealSemiring(3.5)
    b = RealSemiring(3.5)

    assert hash(a) == hash(b)


# ---------------------------------------------------------------------------
# Algebraic laws
# ---------------------------------------------------------------------------

def test_addition_is_commutative():
    a = RealSemiring(3.5)
    b = RealSemiring(2.5)

    assert a + b == b + a


def test_multiplication_is_associative():
    a = RealSemiring(2.0)
    b = RealSemiring(3.0)
    c = RealSemiring(4.0)

    assert (a * b) * c == a * (b * c)


def test_multiplication_distributes_over_addition():
    a = RealSemiring(2.0)
    b = RealSemiring(3.0)
    c = RealSemiring(4.0)

    assert a * (b + c) == (a * b) + (a * c)


# ---------------------------------------------------------------------------
# Invalid operands
# ---------------------------------------------------------------------------

def test_addition_with_invalid_operand():
    a = RealSemiring(3.5)

    with pytest.raises(TypeError):
        a + 2.0


def test_multiplication_with_invalid_operand():
    a = RealSemiring(3.5)

    with pytest.raises(TypeError):
        a * 2.0


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------

def test_repr():
    assert repr(RealSemiring(4.2)) == "ℝ(4.2)"