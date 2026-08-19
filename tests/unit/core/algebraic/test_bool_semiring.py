import pytest

from tests.contracts.core.algebraic.bool_semiring_contracts import (
    ContractedBooleanSemiring,
)

from TARgET.core.algebraic.bool_semiring import BooleanSemiring


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_boolean_semiring_true():
    element = ContractedBooleanSemiring(True)

    assert element.value is True


def test_boolean_semiring_false():
    element = ContractedBooleanSemiring(False)

    assert element.value is False


def test_boolean_semiring_converts_truthy_value():
    element = ContractedBooleanSemiring(1)

    assert element.value is True


def test_boolean_semiring_converts_falsy_value():
    element = ContractedBooleanSemiring(0)

    assert element.value is False


def test_boolean_semiring_converts_empty_string():
    element = ContractedBooleanSemiring("")

    assert element.value is False


def test_boolean_semiring_converts_nonempty_string():
    element = ContractedBooleanSemiring("hello")

    assert element.value is True


# ---------------------------------------------------------------------------
# Zero and one
# ---------------------------------------------------------------------------

def test_zero():
    zero = BooleanSemiring.zero()

    assert isinstance(zero, BooleanSemiring)
    assert zero.value is False


def test_one():
    one = BooleanSemiring.one()

    assert isinstance(one, BooleanSemiring)
    assert one.value is True


def test_zero_is_false():
    assert BooleanSemiring.zero().value is False


def test_one_is_true():
    assert BooleanSemiring.one().value is True


# ---------------------------------------------------------------------------
# Addition
# ---------------------------------------------------------------------------

def test_add_true_true():
    a = BooleanSemiring(True)
    b = BooleanSemiring(True)

    result = a + b

    assert isinstance(result, BooleanSemiring)
    assert result.value is True


def test_add_true_false():
    a = BooleanSemiring(True)
    b = BooleanSemiring(False)

    result = a + b

    assert result.value is True


def test_add_false_true():
    a = BooleanSemiring(False)
    b = BooleanSemiring(True)

    result = a + b

    assert result.value is True


def test_add_false_false():
    a = BooleanSemiring(False)
    b = BooleanSemiring(False)

    result = a + b

    assert result.value is False


# ---------------------------------------------------------------------------
# Multiplication
# ---------------------------------------------------------------------------

def test_mul_true_true():
    a = BooleanSemiring(True)
    b = BooleanSemiring(True)

    result = a * b

    assert isinstance(result, BooleanSemiring)
    assert result.value is True


def test_mul_true_false():
    a = BooleanSemiring(True)
    b = BooleanSemiring(False)

    result = a * b

    assert result.value is False


def test_mul_false_true():
    a = BooleanSemiring(False)
    b = BooleanSemiring(True)

    result = a * b

    assert result.value is False


def test_mul_false_false():
    a = BooleanSemiring(False)
    b = BooleanSemiring(False)

    result = a * b

    assert result.value is False


# ---------------------------------------------------------------------------
# Additive identity
# ---------------------------------------------------------------------------

def test_zero_is_additive_identity_for_true():
    a = BooleanSemiring(True)
    zero = BooleanSemiring.zero()

    assert (a + zero).value is True


def test_zero_is_additive_identity_for_false():
    a = BooleanSemiring(False)
    zero = BooleanSemiring.zero()

    assert (a + zero).value is False


def test_zero_is_additive_identity_on_both_sides():
    for value in (True, False):
        a = BooleanSemiring(value)
        zero = BooleanSemiring.zero()

        assert a + zero == BooleanSemiring(value)
        assert zero + a == BooleanSemiring(value)


# ---------------------------------------------------------------------------
# Multiplicative identity
# ---------------------------------------------------------------------------

def test_one_is_multiplicative_identity_for_true():
    a = BooleanSemiring(True)
    one = BooleanSemiring.one()

    assert (a * one).value is True


def test_one_is_multiplicative_identity_for_false():
    a = BooleanSemiring(False)
    one = BooleanSemiring.one()

    assert (a * one).value is False


def test_one_is_multiplicative_identity_on_both_sides():
    for value in (True, False):
        a = BooleanSemiring(value)
        one = BooleanSemiring.one()

        assert a * one == BooleanSemiring(value)
        assert one * a == BooleanSemiring(value)


# ---------------------------------------------------------------------------
# Zero is absorbing
# ---------------------------------------------------------------------------

def test_zero_absorbs_true():
    a = BooleanSemiring(True)
    zero = BooleanSemiring.zero()

    assert (a * zero).value is False
    assert (zero * a).value is False


def test_zero_absorbs_false():
    a = BooleanSemiring(False)
    zero = BooleanSemiring.zero()

    assert (a * zero).value is False
    assert (zero * a).value is False


# ---------------------------------------------------------------------------
# Algebraic laws
# ---------------------------------------------------------------------------

def test_addition_is_commutative():
    for a_value in (True, False):
        for b_value in (True, False):
            a = BooleanSemiring(a_value)
            b = BooleanSemiring(b_value)

            assert a + b == b + a


def test_addition_is_associative():
    for a_value in (True, False):
        for b_value in (True, False):
            for c_value in (True, False):
                a = BooleanSemiring(a_value)
                b = BooleanSemiring(b_value)
                c = BooleanSemiring(c_value)

                assert (a + b) + c == a + (b + c)


def test_multiplication_is_associative():
    for a_value in (True, False):
        for b_value in (True, False):
            for c_value in (True, False):
                a = BooleanSemiring(a_value)
                b = BooleanSemiring(b_value)
                c = BooleanSemiring(c_value)

                assert (a * b) * c == a * (b * c)


def test_multiplication_distributes_over_addition():
    for a_value in (True, False):
        for b_value in (True, False):
            for c_value in (True, False):
                a = BooleanSemiring(a_value)
                b = BooleanSemiring(b_value)
                c = BooleanSemiring(c_value)

                left = a * (b + c)
                right = (a * b) + (a * c)

                assert left == right


def test_right_distributivity():
    for a_value in (True, False):
        for b_value in (True, False):
            for c_value in (True, False):
                a = BooleanSemiring(a_value)
                b = BooleanSemiring(b_value)
                c = BooleanSemiring(c_value)

                left = (a + b) * c
                right = (a * c) + (b * c)

                assert left == right


# ---------------------------------------------------------------------------
# Closure
# ---------------------------------------------------------------------------

def test_addition_is_closed():
    for a_value in (True, False):
        for b_value in (True, False):
            result = (
                BooleanSemiring(a_value)
                + BooleanSemiring(b_value)
            )

            assert isinstance(result, BooleanSemiring)


def test_multiplication_is_closed():
    for a_value in (True, False):
        for b_value in (True, False):
            result = (
                BooleanSemiring(a_value)
                * BooleanSemiring(b_value)
            )

            assert isinstance(result, BooleanSemiring)


# ---------------------------------------------------------------------------
# Operand type handling
# ---------------------------------------------------------------------------

def test_addition_with_invalid_operand_returns_not_implemented():
    element = BooleanSemiring(True)

    assert element.__add__(True) is NotImplemented


def test_multiplication_with_invalid_operand_returns_not_implemented():
    element = BooleanSemiring(True)

    assert element.__mul__(True) is NotImplemented


def test_addition_with_invalid_operand_raises_type_error():
    element = BooleanSemiring(True)

    with pytest.raises(TypeError):
        element + True


def test_multiplication_with_invalid_operand_raises_type_error():
    element = BooleanSemiring(True)

    with pytest.raises(TypeError):
        element * True


def test_addition_with_none_raises_type_error():
    element = BooleanSemiring(True)

    with pytest.raises(TypeError):
        element + None


def test_multiplication_with_none_raises_type_error():
    element = BooleanSemiring(True)

    with pytest.raises(TypeError):
        element * None


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------

def test_repr_true():
    element = BooleanSemiring(True)

    assert repr(element) == "𝔹(True)"


def test_repr_false():
    element = BooleanSemiring(False)

    assert repr(element) == "𝔹(False)"


# ---------------------------------------------------------------------------
# Fresh zero and one objects
# ---------------------------------------------------------------------------

def test_zero_returns_new_object():
    zero1 = BooleanSemiring.zero()
    zero2 = BooleanSemiring.zero()

    assert zero1 is not zero2
    assert zero1.value == zero2.value


def test_one_returns_new_object():
    one1 = BooleanSemiring.one()
    one2 = BooleanSemiring.one()

    assert one1 is not one2
    assert one1.value == one2.value