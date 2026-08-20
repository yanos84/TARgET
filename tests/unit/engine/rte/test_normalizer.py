import pytest

from tests.contracts.engine.rte.normalizer_contracts import (
    ContractedNormalizer,
)

from TARgET.engine.rte.normalize.normalize import Normalizer

from TARgET.core.rte.rte import (
    Rte,
    Plus,
    CProduct,
    CStar,
    Zero,
    One,
    function,
    Atom,
)

from TARgET.core.base.symbol import Ranked_Symbol

# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

def test_normalizer():
    normalizer = ContractedNormalizer()

    assert isinstance(normalizer, ContractedNormalizer)
    assert isinstance(normalizer, Normalizer)

# ---------------------------------------------------------------------------
# Zero and One
# ---------------------------------------------------------------------------

def test_normalize_zero():
    normalizer = ContractedNormalizer()

    expr = Zero()

    result = normalizer.normalize(expr)

    assert isinstance(result, Zero)
    assert result == expr


def test_normalize_one():
    normalizer = ContractedNormalizer()

    expr = One()

    result = normalizer.normalize(expr)

    assert isinstance(result, One)
    assert result == expr

def test_normalize_zero_is_equal():
    normalizer = ContractedNormalizer()

    assert normalizer.normalize(Zero()) == Zero()


def test_normalize_one_is_equal():
    normalizer = ContractedNormalizer()

    assert normalizer.normalize(One()) == One()

# ---------------------------------------------------------------------------
# Atom
# ---------------------------------------------------------------------------

def test_normalize_atom():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    expr = Atom(a)

    result = normalizer.normalize(expr)

    assert isinstance(result, Atom)
    assert result == expr

# ---------------------------------------------------------------------------
# Function
# ---------------------------------------------------------------------------

def test_normalize_function():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    expr = function(
        f,
        [
            Atom(a),
            Atom(b),
        ],
    )

    result = normalizer.normalize(expr)

    assert isinstance(result, function)
    assert result == expr

def test_normalize_function_arguments():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    expr = function(
        f,
        [
            Plus(
                Zero(),
                Atom(a),
            ),
            Atom(b),
        ],
    )

    result = normalizer.normalize(expr)

    expected = function(
        f,
        [
            Atom(a),
            Atom(b),
        ],
    )

    assert result == expected

# ---------------------------------------------------------------------------
# Plus: zero elimination
# ---------------------------------------------------------------------------

def test_normalize_plus_removes_zero():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)

    expr = Plus(
        Zero(),
        Atom(a),
    )

    result = normalizer.normalize(expr)

    assert result == Atom(a)

def test_normalize_plus_of_only_zero():
    normalizer = ContractedNormalizer()

    expr = Plus(
        Zero(),
        Zero(),
    )

    result = normalizer.normalize(expr)

    assert isinstance(result, Zero)

def test_normalize_plus_removes_duplicates():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)

    expr = Plus(
        Atom(a),
        Atom(a),
    )

    result = normalizer.normalize(expr)

    assert result == Atom(a)

def test_normalize_plus_flattens_nested_plus():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = Plus(
        Atom(a),
        Plus(
            Atom(b),
            Atom(a),
        ),
    )

    result = normalizer.normalize(expr)

    expected = Plus(
        Atom(a),
        Atom(b),
    )

    assert result == expected

def test_normalize_nested_plus_removes_zero():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)

    expr = Plus(
        Zero(),
        Plus(
            Zero(),
            Atom(a),
        ),
    )

    result = normalizer.normalize(expr)

    assert result == Atom(a)


def test_normalize_plus_has_canonical_order():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    left = normalizer.normalize(
        Plus(
            Atom(a),
            Atom(b),
        )
    )

    right = normalizer.normalize(
        Plus(
            Atom(b),
            Atom(a),
        )
    )

    assert left == right
    assert str(left) == str(right)

# ---------------------------------------------------------------------------
# CProduct
# ---------------------------------------------------------------------------

def test_normalize_cproduct_zero_left():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Zero(),
        Atom(a),
        c,
    )

    result = normalizer.normalize(expr)

    assert isinstance(result, Zero)

def test_normalize_cproduct_zero_right():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Atom(a),
        Zero(),
        c,
    )

    result = normalizer.normalize(expr)

    assert isinstance(result, Zero)

def test_normalize_cproduct_one_left():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        One(),
        Atom(a),
        c,
    )

    result = normalizer.normalize(expr)

    assert result == Atom(a)

def test_normalize_cproduct_one_right():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Atom(a),
        One(),
        c,
    )

    result = normalizer.normalize(expr)

    assert result == Atom(a)

def test_normalize_cproduct():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Atom(a),
        Atom(b),
        c,
    )

    result = normalizer.normalize(expr)

    expected = CProduct(
        Atom(a),
        Atom(b),
        c,
    )

    assert result == expected

def test_normalize_cproduct_recursively():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Plus(
            Zero(),
            Atom(a),
        ),
        Atom(b),
        c,
    )

    result = normalizer.normalize(expr)

    expected = CProduct(
        Atom(a),
        Atom(b),
        c,
    )

    assert result == expected

# ---------------------------------------------------------------------------
# CStar
# ---------------------------------------------------------------------------

def test_normalize_cstar_zero():
    normalizer = ContractedNormalizer()

    c = Ranked_Symbol("c", 0)

    expr = CStar(
        Zero(),
        c,
    )

    result = normalizer.normalize(expr)

    assert isinstance(result, One)

def test_normalize_cstar_one():
    normalizer = ContractedNormalizer()

    c = Ranked_Symbol("c", 0)

    expr = CStar(
        One(),
        c,
    )

    result = normalizer.normalize(expr)

    assert isinstance(result, One)

def test_normalize_cstar():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CStar(
        Atom(a),
        c,
    )

    result = normalizer.normalize(expr)

    expected = CStar(
        Atom(a),
        c,
    )

    assert result == expected

def test_normalize_nested_cstar_same_concat():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CStar(
        CStar(
            Atom(a),
            c,
        ),
        c,
    )

    result = normalizer.normalize(expr)

    expected = CStar(
        Atom(a),
        c,
    )

    assert result == expected

def test_normalize_nested_cstar_different_concat():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)
    d = Ranked_Symbol("d", 0)

    expr = CStar(
        CStar(
            Atom(a),
            c,
        ),
        d,
    )

    result = normalizer.normalize(expr)

    expected = CStar(
        CStar(
            Atom(a),
            c,
        ),
        d,
    )

    assert result == expected

def test_normalize_example():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = Plus(
        Atom(a),
        Plus(
            Atom(a),
            Atom(b),
        ),
    )

    result = normalizer.normalize(expr)

    expected = Plus(
        Atom(a),
        Atom(b),
    )

    assert result == expected

def test_normalize_example_zero_plus_function():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)

    expr = Plus(
        Zero(),
        function(a, []),
    )

    result = normalizer.normalize(expr)

    assert result == function(a, [])

def test_normalize_example_one_cproduct():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = CProduct(
        One(),
        function(b, []),
        a,
    )

    result = normalizer.normalize(expr)

    assert result == function(b, [])

def test_normalize_example_zero_cstar():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)

    expr = CStar(
        Zero(),
        a,
    )

    result = normalizer.normalize(expr)

    assert result == One()

def test_normalize_example_nested_cstar():
    normalizer = ContractedNormalizer()

    a = Ranked_Symbol("a", 0)

    expr = CStar(
        CStar(
            function(a, []),
            a,
        ),
        a,
    )

    result = normalizer.normalize(expr)

    expected = CStar(
        function(a, []),
        a,
    )

    assert result == expected