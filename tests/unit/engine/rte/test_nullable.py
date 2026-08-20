from tests.contracts.engine.rte.nullable_contracts import (
    contracted_nullable,
)

from TARgET.core.rte.rte import (
    Rte,
    Zero,
    One,
    Plus,
    CProduct,
    CStar,
    function,
    Atom,
)

from TARgET.core.base.symbol import Ranked_Symbol

# ---------------------------------------------------------------------------
# Zero and One
# ---------------------------------------------------------------------------

def test_nullable_zero():
    expr = Zero()

    assert contracted_nullable(expr) is False


def test_nullable_one():
    expr = One()

    assert contracted_nullable(expr) is True

# ---------------------------------------------------------------------------
# Atom
# ---------------------------------------------------------------------------

def test_nullable_atom():
    a = Ranked_Symbol("a", 0)

    expr = Atom(a)

    assert contracted_nullable(expr) is False

def test_nullable_different_atoms():
    for name in ("a", "b", "x"):
        expr = Atom(Ranked_Symbol(name, 0))

        assert contracted_nullable(expr) is False

# ---------------------------------------------------------------------------
# Function
# ---------------------------------------------------------------------------

def test_nullable_function():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 1)

    expr = function(
        f,
        [Atom(a)],
    )

    assert contracted_nullable(expr) is False

def test_nullable_nullary_function():
    a = Ranked_Symbol("a", 0)

    expr = function(a, [])

    assert contracted_nullable(expr) is False

def test_nullable_function_with_multiple_arguments():
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

    assert contracted_nullable(expr) is False

# ---------------------------------------------------------------------------
# Plus
# ---------------------------------------------------------------------------

def test_nullable_plus_false():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = Plus(
        Atom(a),
        Atom(b),
    )

    assert contracted_nullable(expr) is False

def test_nullable_plus_true():
    a = Ranked_Symbol("a", 0)

    expr = Plus(
        Atom(a),
        One(),
    )

    assert contracted_nullable(expr) is True

def test_nullable_plus_nullable_first():
    a = Ranked_Symbol("a", 0)

    expr = Plus(
        One(),
        Atom(a),
    )

    assert contracted_nullable(expr) is True

def test_nullable_plus_multiple_nullable_terms():
    a = Ranked_Symbol("a", 0)

    expr = Plus(
        One(),
        Atom(a),
        One(),
    )

    assert contracted_nullable(expr) is True

def test_nullable_nested_plus():
    a = Ranked_Symbol("a", 0)

    expr = Plus(
        Atom(a),
        Plus(
            Atom(a),
            One(),
        ),
    )

    assert contracted_nullable(expr) is True

# ---------------------------------------------------------------------------
# CProduct
# ---------------------------------------------------------------------------

def test_nullable_cproduct_false_false():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Atom(a),
        Atom(b),
        c,
    )

    assert contracted_nullable(expr) is False

def test_nullable_cproduct_true_false():
    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        One(),
        Atom(a),
        c,
    )

    assert contracted_nullable(expr) is False

def test_nullable_cproduct_false_true():
    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        Atom(a),
        One(),
        c,
    )

    assert contracted_nullable(expr) is False

def test_nullable_cproduct_true_true():
    c = Ranked_Symbol("c", 0)

    expr = CProduct(
        One(),
        One(),
        c,
    )

    assert contracted_nullable(expr) is True

# ---------------------------------------------------------------------------
# CStar
# ---------------------------------------------------------------------------

def test_nullable_cstar_atom():
    a = Ranked_Symbol("a", 0)
    c = Ranked_Symbol("c", 0)

    expr = CStar(
        Atom(a),
        c,
    )

    assert contracted_nullable(expr) is True

def test_nullable_cstar_zero():
    c = Ranked_Symbol("c", 0)

    expr = CStar(
        Zero(),
        c,
    )

    assert contracted_nullable(expr) is True

def test_nullable_cstar_one():
    c = Ranked_Symbol("c", 0)

    expr = CStar(
        One(),
        c,
    )

    assert contracted_nullable(expr) is True

def test_nullable_cstar_function():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 1)
    c = Ranked_Symbol("c", 0)

    expr = CStar(
        function(
            f,
            [Atom(a)],
        ),
        c,
    )

    assert contracted_nullable(expr) is True

# ---------------------------------------------------------------------------
# Complex expressions
# ---------------------------------------------------------------------------

def test_nullable_complex_rte():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    fab = function(
        f,
        [
            Atom(a),
            Atom(b),
        ],
    )

    expr = Plus(
        CStar(fab, a),
        CProduct(
            fab,
            fab,
            a,
        ),
    )

    assert contracted_nullable(expr) is True

def test_nullable_complex_rte_false():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    fab = function(
        f,
        [
            Atom(a),
            Atom(b),
        ],
    )

    expr = Plus(
        fab,
        CProduct(
            fab,
            Atom(a),
            a,
        ),
    )

    assert contracted_nullable(expr) is False

def test_nullable_always_returns_bool():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    expressions = [
        Zero(),
        One(),
        Atom(a),
        function(f, [Atom(a), Atom(b)]),
        Plus(Atom(a), One()),
        CProduct(One(), Atom(a), a),
        CStar(Atom(a), a),
    ]

    for expr in expressions:
        result = contracted_nullable(expr)

        assert isinstance(result, bool)