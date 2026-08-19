import pytest

from tests.contracts.core.algebraic.integer_semiring_contracts import (
    ContractedIntegerSemiring,
)

from TARgET.core.algebraic.integer_semiring import IntegerSemiring


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_integer_semiring_construction():
    element = ContractedIntegerSemiring(5)

    assert element.value == 5


def test_integer_semiring_converts_value_to_int():
    element = ContractedIntegerSemiring("5")

    assert element.value == 5


# ---------------------------------------------------------------------------
# Zero and one
# ---------------------------------------------------------------------------

def test_zero():
    zero = IntegerSemiring.zero()

    assert zero.value == 0


def test_one():
    one = IntegerSemiring.one()

    assert one.value == 1


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def test_addition():
    a = IntegerSemiring(3)
    b = IntegerSemiring(5)

    result = a + b

    assert result == IntegerSemiring(8)


def test_multiplication():
    a = IntegerSemiring(3)
    b = IntegerSemiring(5)

    result = a * b

    assert result == IntegerSemiring(15)


# ---------------------------------------------------------------------------
# Semiring identities
# ---------------------------------------------------------------------------

def test_zero_is_additive_identity():
    a = IntegerSemiring(7)
    zero = IntegerSemiring.zero()

    assert a + zero == a
    assert zero + a == a


def test_one_is_multiplicative_identity():
    a = IntegerSemiring(7)
    one = IntegerSemiring.one()

    assert a * one == a
    assert one * a == a


def test_zero_is_multiplicatively_absorbing():
    a = IntegerSemiring(7)
    zero = IntegerSemiring.zero()

    assert a * zero == zero
    assert zero * a == zero


# ---------------------------------------------------------------------------
# Equality and hashing
# ---------------------------------------------------------------------------

def test_equal_integer_elements():
    a = IntegerSemiring(5)
    b = IntegerSemiring(5)

    assert a == b


def test_different_integer_elements():
    a = IntegerSemiring(5)
    b = IntegerSemiring(6)

    assert a != b


def test_equal_integer_elements_have_same_hash():
    a = IntegerSemiring(5)
    b = IntegerSemiring(5)

    assert hash(a) == hash(b)


# ---------------------------------------------------------------------------
# Algebraic laws
# ---------------------------------------------------------------------------

def test_addition_is_commutative():
    a = IntegerSemiring(3)
    b = IntegerSemiring(5)

    assert a + b == b + a


def test_multiplication_is_associative():
    a = IntegerSemiring(2)
    b = IntegerSemiring(3)
    c = IntegerSemiring(4)

    assert (a * b) * c == a * (b * c)


def test_multiplication_distributes_over_addition():
    a = IntegerSemiring(2)
    b = IntegerSemiring(3)
    c = IntegerSemiring(4)

    assert a * (b + c) == (a * b) + (a * c)


# ---------------------------------------------------------------------------
# Invalid operands
# ---------------------------------------------------------------------------

def test_addition_with_invalid_operand():
    a = IntegerSemiring(5)

    with pytest.raises(TypeError):
        a + 2


def test_multiplication_with_invalid_operand():
    a = IntegerSemiring(5)

    with pytest.raises(TypeError):
        a * 2


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------

def test_repr():
    element = IntegerSemiring(42)

    assert repr(element) == "ℤ(42)"