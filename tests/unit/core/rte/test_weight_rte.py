import pytest

from tests.contracts.core.rte.weight_rte_contracts import (
    ContractedWeight,
)

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

from TARgET.core.rte.weighted.weight import Weight
from TARgET.core.rte.weighted.weighting import (
    RteWeighting,
    SemiringRteWeighting,
)
from TARgET.core.rte.weighted.weight_rte_print import (
    WeightedRtePrinter,
)

from TARgET.core.algebraic.trop_semiring import TropicalSemiring
from TARgET.core.base.symbol import Ranked_Symbol

# ---------------------------------------------------------------------------
# Weight construction
# ---------------------------------------------------------------------------

def test_weight():
    a = Ranked_Symbol("a", 0)

    expr = Atom(a)
    weight = TropicalSemiring(2.0)

    weighted = ContractedWeight(weight, expr)

    assert isinstance(weighted, Rte)
    assert isinstance(weighted, Weight)
    assert weighted.weight == weight
    assert weighted.expr == expr

def test_weight_string():
    a = Ranked_Symbol("a", 0)

    weighted = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    assert str(weighted) == "𝕋(2.0) ⊗ (a)"

def test_weight_string():
    a = Ranked_Symbol("a", 0)

    weighted = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    assert str(weighted) == "𝕋(2.0) ⊗ (a)"

def test_weight_equality():
    a = Ranked_Symbol("a", 0)

    left = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    right = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    assert left == right

def test_weights_with_different_values_are_not_equal():
    a = Ranked_Symbol("a", 0)

    left = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    right = ContractedWeight(
        TropicalSemiring(3.0),
        Atom(a),
    )

    assert left != right

def test_weights_with_different_expressions_are_not_equal():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    left = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    right = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(b),
    )

    assert left != right

def test_equal_weights_have_equal_hashes():
    a = Ranked_Symbol("a", 0)

    left = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    right = ContractedWeight(
        TropicalSemiring(2.0),
        Atom(a),
    )

    assert left == right
    assert hash(left) == hash(right)

# ---------------------------------------------------------------------------
# Zero and One
# ---------------------------------------------------------------------------

def test_weight_zero():
    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(Zero())

    assert isinstance(result, TropicalSemiring)
    assert result == TropicalSemiring.zero()

def test_weight_one():
    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(One())

    assert isinstance(result, TropicalSemiring)
    assert result == TropicalSemiring.one()

def test_weight_atom_is_one():
    a = Ranked_Symbol("a", 0)

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(Atom(a))

    assert result == TropicalSemiring.one()

def test_weight_function_is_one():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    f = Ranked_Symbol("f", 2)

    expr = function(
        f,
        [Atom(a), Atom(b)],
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring.one()

# ---------------------------------------------------------------------------
# Plus
# ---------------------------------------------------------------------------

def test_weight_plus():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = Plus(
        Atom(a),
        Atom(b),
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring.one()

def test_weight_nested_plus():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = Plus(
        Atom(a),
        Plus(
            Atom(b),
            Atom(a),
        ),
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring.one()

# ---------------------------------------------------------------------------
# CProduct
# ---------------------------------------------------------------------------

def test_weight_cproduct():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)
    concat = Ranked_Symbol("c", 0)

    expr = CProduct(
        Atom(a),
        Atom(b),
        concat,
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring.one()

# ---------------------------------------------------------------------------
# CStar
# ---------------------------------------------------------------------------

def test_weight_cstar():
    a = Ranked_Symbol("a", 0)
    concat = Ranked_Symbol("c", 0)

    expr = CStar(
        Atom(a),
        concat,
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring.one()

# ---------------------------------------------------------------------------
# Weighted RTE
# ---------------------------------------------------------------------------

def test_weighted_rte():
    a = Ranked_Symbol("a", 0)

    expr = ContractedWeight(
        TropicalSemiring(3.0),
        Atom(a),
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring(3.0)

def test_nested_weighted_rte():
    a = Ranked_Symbol("a", 0)

    expr = ContractedWeight(
        TropicalSemiring(1.0),
        ContractedWeight(
            TropicalSemiring(2.0),
            Atom(a),
        ),
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring(3.0)

# ---------------------------------------------------------------------------
# Complex weighted RTE
# ---------------------------------------------------------------------------

def test_complex_weighted_rte():
    f = Ranked_Symbol("f", 2)
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    expr = ContractedWeight(
        TropicalSemiring(1.0),
        ContractedWeight(
            TropicalSemiring(2.0),
            Plus(
                function(f, [Atom(a), Atom(b)]),
                function(f, [Atom(b), Atom(a)]),
            ),
        ),
    )

    weighting = SemiringRteWeighting(TropicalSemiring)

    result = weighting.weight(expr)

    assert result == TropicalSemiring(3.0)