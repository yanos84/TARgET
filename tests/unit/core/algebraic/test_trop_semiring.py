import math
import pytest

from tests.contracts.core.algebraic.trop_semiring_contracts import (
    ContractedTropicalSemiring,
)

from TARgET.core.algebraic.trop_semiring import TropicalSemiring


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_tropical_construction():
    element = ContractedTropicalSemiring(3.5)

    assert element.value == 3.5


def test_tropical_accepts_infinity():
    element = TropicalSemiring(math.inf)

    assert element.value == math.inf


def test_tropical_accepts_negative_value():
    element = TropicalSemiring(-3.5)

    assert element.value == -3.5


# ---------------------------------------------------------------------------
# Zero and one
# ---------------------------------------------------------------------------

def test_zero():
    zero = TropicalSemiring.zero()

    assert zero.value == math.inf


def test_one():
    one = TropicalSemiring.one()

    assert one.value == 0.0


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def test_addition_is_minimum():
    a = TropicalSemiring(3.0)
    b = TropicalSemiring(5.0)

    assert a + b == TropicalSemiring(3.0)


def test_multiplication_is_addition():
    a = TropicalSemiring(3.0)
    b = TropicalSemiring(5.0)

    assert a * b == TropicalSemiring(8.0)


# ---------------------------------------------------------------------------
# Identities
# ---------------------------------------------------------------------------

def test_zero_is_additive_identity():
    a = TropicalSemiring(3.0)
    zero = TropicalSemiring.zero()

    assert a + zero == a
    assert zero + a == a


def test_one_is_multiplicative_identity():
    a = TropicalSemiring(3.0)
    one = TropicalSemiring.one()

    assert a * one == a
    assert one * a == a


def test_zero_is_multiplicatively_absorbing():
    a = TropicalSemiring(3.0)
    zero = TropicalSemiring.zero()

    assert a * zero == zero
    assert zero * a == zero


# ---------------------------------------------------------------------------
# Equality and hashing
# ---------------------------------------------------------------------------

def test_equal_tropical_elements():
    assert TropicalSemiring(3.0) == TropicalSemiring(3.0)


def test_different_tropical_elements():
    assert TropicalSemiring(3.0) != TropicalSemiring(5.0)


def test_equal_tropical_elements_have_same_hash():
    a = TropicalSemiring(3.0)
    b = TropicalSemiring(3.0)

    assert hash(a) == hash(b)


# ---------------------------------------------------------------------------
# Algebraic laws
# ---------------------------------------------------------------------------

def test_addition_is_commutative():
    a = TropicalSemiring(3.0)
    b = TropicalSemiring(5.0)

    assert a + b == b + a


def test_addition_is_associative():
    a = TropicalSemiring(3.0)
    b = TropicalSemiring(5.0)
    c = TropicalSemiring(2.0)

    assert (a + b) + c == a + (b + c)


def test_multiplication_is_associative():
    a = TropicalSemiring(2.0)
    b = TropicalSemiring(3.0)
    c = TropicalSemiring(4.0)

    assert (a * b) * c == a * (b * c)


def test_multiplication_distributes_over_addition():
    a = TropicalSemiring(2.0)
    b = TropicalSemiring(3.0)
    c = TropicalSemiring(5.0)

    assert a * (b + c) == (a * b) + (a * c)


# ---------------------------------------------------------------------------
# Infinity edge cases
# ---------------------------------------------------------------------------

def test_min_with_infinity():
    a = TropicalSemiring(4.0)
    infinity = TropicalSemiring.zero()

    assert a + infinity == a


def test_infinity_plus_infinity():
    infinity = TropicalSemiring.zero()

    assert infinity + infinity == infinity


def test_infinity_times_finite_value():
    infinity = TropicalSemiring.zero()
    a = TropicalSemiring(4.0)

    assert infinity * a == infinity


# ---------------------------------------------------------------------------
# Invalid operands
# ---------------------------------------------------------------------------

def test_addition_with_invalid_operand():
    with pytest.raises(TypeError):
        TropicalSemiring(3.0) + 2.0


def test_multiplication_with_invalid_operand():
    with pytest.raises(TypeError):
        TropicalSemiring(3.0) * 2.0


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------

def test_repr_finite_value():
    assert repr(TropicalSemiring(3.0)) == "𝕋(3.0)"


def test_repr_infinity():
    assert repr(TropicalSemiring.zero()) == "𝕋(∞)"