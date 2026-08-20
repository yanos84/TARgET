import pytest
from TARgET.core.base.symbol import Ranked_Symbol, Symbol
from TARgET.core.rte.rte import (
    Rte,
    Zero,
    One,
    Atom,
    function,
    Plus,
    CProduct,
    CStar,
)

from tests.contracts.core.rte.rte_contracts import (
    ContractedZero,
    ContractedOne,
    ContractedAtom,
    ContractedFunction,
    ContractedPlus,
    ContractedCProduct,
    ContractedCStar,
)

# ---------------------------------------------------------------------------
# Zero
# ---------------------------------------------------------------------------

def test_zero():
    zero = ContractedZero()

    assert isinstance(zero, Rte)
    assert isinstance(zero, Zero)
    assert str(zero) == "0"


# ---------------------------------------------------------------------------
# One
# ---------------------------------------------------------------------------

def test_one():
    one = ContractedOne()

    assert isinstance(one, Rte)
    assert isinstance(one, One)
    assert str(one) == "1"


def test_zero_and_one_are_different():
    assert ContractedZero() != ContractedOne()

# ---------------------------------------------------------------------------
# Atom
# ---------------------------------------------------------------------------

def test_atom():
    a = Ranked_Symbol("a", 0)

    atom = ContractedAtom(a)

    assert isinstance(atom, Rte)
    assert isinstance(atom, Atom)
    assert atom.symbol == a
    assert str(atom) == "a"


def test_atom_equality():
    a = Ranked_Symbol("a", 0)

    left = ContractedAtom(a)
    right = ContractedAtom(a)

    assert left == right


def test_atoms_with_different_symbols_are_not_equal():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    assert ContractedAtom(a) != ContractedAtom(b)


def test_atom_rejects_non_leaf_ranked_symbol():
    f = Ranked_Symbol("f", 2)

    with pytest.raises(ValueError):
        ContractedAtom(f)


# ---------------------------------------------------------------------------
# Function
# ---------------------------------------------------------------------------

def test_function():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    expr = ContractedFunction(
        f,
        [
            ContractedAtom(a),
            ContractedAtom(b),
        ],
    )

    assert isinstance(expr, Rte)
    assert isinstance(expr, function)
    assert expr.symbol == f
    assert len(expr.args) == 2
    assert str(expr) == "f(a,b)"

def test_unary_function():
    a = Ranked_Symbol("a", 0)
    g = Ranked_Symbol("g", 1)

    expr = ContractedFunction(
        g,
        [ContractedAtom(a)],
    )

    assert str(expr) == "g(a)"

def test_nested_function():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 2)
    g = Ranked_Symbol("g", 1)

    inner = ContractedFunction(
        g,
        [ContractedAtom(a)],
    )

    expr = ContractedFunction(
        f,
        [inner, ContractedAtom(a)],
    )

    assert str(expr) == "f(g(a),a)"

def test_function_with_too_few_arguments():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 2)

    with pytest.raises(ValueError):
        ContractedFunction(
            f,
            [ContractedAtom(a)],
        )


def test_function_with_too_many_arguments():
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 2)

    with pytest.raises(ValueError):
        ContractedFunction(
            f,
            [
                ContractedAtom(a),
                ContractedAtom(a),
                ContractedAtom(a),
            ],
        )

def test_function_with_rank_zero_symbol():
    a = Ranked_Symbol("a", 0)

    expr = ContractedFunction(a)

    assert str(expr) == "a"

# ---------------------------------------------------------------------------
# Plus
# ---------------------------------------------------------------------------

def test_plus():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = ContractedPlus(
        ContractedAtom(a),
        ContractedAtom(b),
    )

    assert isinstance(expr, Rte)
    assert isinstance(expr, Plus)
    assert len(expr.terms) == 2
    assert str(expr) == "a + b"

def test_plus_removes_duplicates():
    a = Ranked_Symbol("a", 0)

    expr = ContractedPlus(
        ContractedAtom(a),
        ContractedAtom(a),
    )

    assert len(expr.terms) == 1
    assert expr.terms[0] == ContractedAtom(a)

def test_plus_flattens_nested_plus():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = ContractedPlus(
        ContractedAtom(a),
        ContractedPlus(
            ContractedAtom(b),
            ContractedAtom(a),
        ),
    )

    assert len(expr.terms) == 2
    assert all(not isinstance(term, Plus) for term in expr.terms)

def test_plus_is_commutative():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    left = ContractedPlus(
        ContractedAtom(a),
        ContractedAtom(b),
    )

    right = ContractedPlus(
        ContractedAtom(b),
        ContractedAtom(a),
    )

    assert left == right

def test_equal_plus_expressions_have_equal_hashes():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    left = ContractedPlus(
        ContractedAtom(a),
        ContractedAtom(b),
    )

    right = ContractedPlus(
        ContractedAtom(b),
        ContractedAtom(a),
    )

    assert left == right
    assert hash(left) == hash(right)

# ---------------------------------------------------------------------------
# CProduct
# ---------------------------------------------------------------------------

def test_cproduct():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    concat = Ranked_Symbol("c", 0)

    expr = ContractedCProduct(
        ContractedAtom(a),
        ContractedAtom(b),
        concat,
    )

    assert isinstance(expr, Rte)
    assert isinstance(expr, CProduct)
    assert expr.left == ContractedAtom(a)
    assert expr.right == ContractedAtom(b)
    assert expr.concat == concat
    assert str(expr) == "(a).c(b)"

def test_cproduct_equality():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    concat = Ranked_Symbol(".", 0)

    left = ContractedCProduct(
        ContractedAtom(a),
        ContractedAtom(b),
        concat,
    )

    right = ContractedCProduct(
        ContractedAtom(a),
        ContractedAtom(b),
        concat,
    )

    assert left == right
    assert hash(left) == hash(right)

def test_cproduct_rejects_non_symbol_concat():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    with pytest.raises(ValueError):
        ContractedCProduct(
            ContractedAtom(a),
            ContractedAtom(b),
            "not_a_symbol",
        )

# ---------------------------------------------------------------------------
# CStar
# ---------------------------------------------------------------------------

def test_cstar():
    a = Ranked_Symbol("a", 0)
    concat = Ranked_Symbol(".", 0)

    expr = ContractedCStar(
        ContractedAtom(a),
        concat,
    )

    assert isinstance(expr, Rte)
    assert isinstance(expr, CStar)
    assert expr.expr == ContractedAtom(a)
    assert expr.concat == concat
    assert str(expr) == "(a)*."

def test_cstar_equality():
    a = Ranked_Symbol("a", 0)
    concat = Ranked_Symbol(".", 0)

    left = ContractedCStar(
        ContractedAtom(a),
        concat,
    )

    right = ContractedCStar(
        ContractedAtom(a),
        concat,
    )

    assert left == right
    assert hash(left) == hash(right)

# ---------------------------------------------------------------------------
# Complex RTE
# ---------------------------------------------------------------------------

def test_complex_rte():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    x = Ranked_Symbol("x", 0)

    f = Ranked_Symbol("f", 2)
    g = Ranked_Symbol("g", 1)

    fab = ContractedFunction(
        f,
        [
            ContractedAtom(a),
            ContractedAtom(b),
        ],
    )

    gx = ContractedFunction(
        g,
        [ContractedAtom(x)],
    )

    expr = ContractedPlus(
        ContractedCStar(fab, b),
        ContractedCProduct(fab, gx, a),
    )

    assert isinstance(expr, Rte)
    assert isinstance(expr, Plus)
    assert len(expr.terms) == 2

def test_complex_rte_string():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    x = Ranked_Symbol("x", 0)

    f = Ranked_Symbol("f", 2)
    g = Ranked_Symbol("g", 1)

    fab = ContractedFunction(
        f,
        [
            ContractedAtom(a),
            ContractedAtom(b),
        ],
    )

    gx = ContractedFunction(
        g,
        [ContractedAtom(x)],
    )

    expr = ContractedPlus(
        ContractedCStar(fab, b),
        ContractedCProduct(fab, gx, a),
    )

    assert str(expr) == (
        "(f(a,b)).a(g(x)) + "
        "(f(a,b))*b"
    )