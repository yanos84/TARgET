import pytest
import icontract

from tests.contracts.core.base.tree_contracts import (
    ContractedTree,
    ContractedRankedTree,
    ContractedUnrankedTree,
)

from TARgET.core.base.symbol import Ranked_Symbol


# ---------------------------------------------------------------------------
# AbstractTree construction
# ---------------------------------------------------------------------------

def test_tree_construction():
    tree = ContractedTree("a")

    assert tree.symbol == "a"
    assert tree.children == []
    assert tree.parent is None


def test_tree_empty_symbol():
    tree = ContractedTree("")

    assert tree.symbol == ""
    assert str(tree) == ""


def test_tree_long_symbol():
    symbol = "a" * 10_000
    tree = ContractedTree(symbol)

    assert tree.symbol == symbol
    assert str(tree) == symbol


# ---------------------------------------------------------------------------
# AbstractTree children
# ---------------------------------------------------------------------------

def test_add_child():
    parent = ContractedTree("f")
    child = ContractedTree("a")

    parent.add_child(child)

    assert parent.children == [child]
    assert child.parent is parent


def test_add_multiple_children():
    parent = ContractedTree("f")
    child1 = ContractedTree("a")
    child2 = ContractedTree("b")
    child3 = ContractedTree("c")

    parent.add_child(child1)
    parent.add_child(child2)
    parent.add_child(child3)

    assert parent.children == [child1, child2, child3]


def test_add_child_rejects_non_tree():
    tree = ContractedTree("f")

    with pytest.raises(TypeError):
        tree.add_child("a")


def test_add_child_rejects_none():
    tree = ContractedTree("f")

    with pytest.raises(TypeError):
        tree.add_child(None)


# ---------------------------------------------------------------------------
# Parent-child relationship
# ---------------------------------------------------------------------------

def test_child_parent_relationship():
    parent = ContractedTree("f")
    child = ContractedTree("a")

    parent.add_child(child)

    assert child.parent is parent
    assert parent.parent is None


def test_nested_parent_child_relationship():
    root = ContractedTree("f")
    child = ContractedTree("g")
    grandchild = ContractedTree("a")

    root.add_child(child)
    child.add_child(grandchild)

    assert child.parent is root
    assert grandchild.parent is child
    assert root.parent is None


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------

def test_leaf_string_representation():
    tree = ContractedTree("a")

    assert str(tree) == "a"


def test_tree_string_representation():
    root = ContractedTree("f")
    child1 = ContractedTree("a")
    child2 = ContractedTree("b")

    root.add_child(child1)
    root.add_child(child2)

    assert str(root) == "f(a,b)"


def test_nested_tree_string_representation():
    root = ContractedTree("f")
    child = ContractedTree("g")
    grandchild = ContractedTree("a")

    root.add_child(child)
    child.add_child(grandchild)

    assert str(root) == "f(g(a))"


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

def test_leaf_structure():
    tree = ContractedTree("a")

    assert tree.structure() == ("a", ())


def test_tree_structure():
    root = ContractedTree("f")
    child1 = ContractedTree("a")
    child2 = ContractedTree("b")

    root.add_child(child1)
    root.add_child(child2)

    assert root.structure() == (
        "f",
        (
            ("a", ()),
            ("b", ()),
        ),
    )


def test_nested_tree_structure():
    root = ContractedTree("f")
    child = ContractedTree("g")
    grandchild = ContractedTree("a")

    root.add_child(child)
    child.add_child(grandchild)

    assert root.structure() == (
        "f",
        (
            (
                "g",
                (
                    ("a", ()),
                ),
            ),
        ),
    )


# ---------------------------------------------------------------------------
# RankedTree construction
# ---------------------------------------------------------------------------

def test_ranked_tree_construction():
    symbol = Ranked_Symbol("a", 0)
    tree = ContractedRankedTree(symbol)

    assert tree.symbol == "a"
    assert tree.ranked_symbol == symbol
    assert tree.children == []
    assert tree.parent is None


def test_ranked_tree_preserves_symbol_rank():
    symbol = Ranked_Symbol("f", 2)
    tree = ContractedRankedTree(symbol)

    assert tree.ranked_symbol.rank == 2


# ---------------------------------------------------------------------------
# RankedTree well-formedness
# ---------------------------------------------------------------------------

def test_ranked_leaf_is_well_formed():
    symbol = Ranked_Symbol("a", 0)
    tree = ContractedRankedTree(symbol)

    assert tree.is_well_formed() is True


def test_ranked_tree_is_not_well_formed_when_missing_children():
    symbol = Ranked_Symbol("f", 2)
    tree = ContractedRankedTree(symbol)

    assert tree.is_well_formed() is False


def test_ranked_tree_is_well_formed_with_correct_number_of_children():
    f = Ranked_Symbol("f", 2)
    a = Ranked_Symbol("a", 0)

    root = ContractedRankedTree(f)
    child1 = ContractedRankedTree(a)
    child2 = ContractedRankedTree(a)

    root.add_child(child1)
    root.add_child(child2)

    assert root.is_well_formed() is True


# ---------------------------------------------------------------------------
# RankedTree rank enforcement
# ---------------------------------------------------------------------------

def test_ranked_tree_rejects_child_above_rank():
    f = Ranked_Symbol("f", 1)
    a = Ranked_Symbol("a", 0)

    root = ContractedRankedTree(f)
    child1 = ContractedRankedTree(a)
    child2 = ContractedRankedTree(a)

    root.add_child(child1)

    with pytest.raises(ValueError):
        root.add_child(child2)


def test_ranked_tree_rank_zero_rejects_children():
    a = Ranked_Symbol("a", 0)
    b = Ranked_Symbol("b", 0)

    root = ContractedRankedTree(a)
    child = ContractedRankedTree(b)

    with pytest.raises(ValueError):
        root.add_child(child)


def test_ranked_tree_accepts_exact_rank():
    f = Ranked_Symbol("f", 3)
    a = Ranked_Symbol("a", 0)

    root = ContractedRankedTree(f)

    root.add_child(ContractedRankedTree(a))
    root.add_child(ContractedRankedTree(a))
    root.add_child(ContractedRankedTree(a))

    assert len(root.children) == 3
    assert root.is_well_formed() is True


# ---------------------------------------------------------------------------
# RankedTree child type
# ---------------------------------------------------------------------------

def test_ranked_tree_rejects_non_tree_child():
    f = Ranked_Symbol("f", 1)
    root = ContractedRankedTree(f)

    with pytest.raises(TypeError):
        root.add_child("a")


def test_ranked_tree_rejects_none_child():
    f = Ranked_Symbol("f", 1)
    root = ContractedRankedTree(f)

    with pytest.raises(TypeError):
        root.add_child(None)


# ---------------------------------------------------------------------------
# RankedTree malformed child
# ---------------------------------------------------------------------------

def test_ranked_tree_is_not_well_formed_if_child_is_not_well_formed():
    f = Ranked_Symbol("f", 1)
    g = Ranked_Symbol("g", 2)
    a = Ranked_Symbol("a", 0)

    root = ContractedRankedTree(f)
    child = ContractedRankedTree(g)
    grandchild = ContractedRankedTree(a)

    root.add_child(child)
    child.add_child(grandchild)

    assert child.is_well_formed() is False
    assert root.is_well_formed() is False


# ---------------------------------------------------------------------------
# UnrankedTree construction
# ---------------------------------------------------------------------------

def test_unranked_tree_construction():
    tree = ContractedUnrankedTree("a")

    assert tree.symbol == "a"
    assert tree.children == []
    assert tree.parent is None


# ---------------------------------------------------------------------------
# UnrankedTree children
# ---------------------------------------------------------------------------

def test_unranked_tree_accepts_multiple_children():
    root = ContractedUnrankedTree("f")

    root.add_child(ContractedUnrankedTree("a"))
    root.add_child(ContractedUnrankedTree("b"))
    root.add_child(ContractedUnrankedTree("c"))

    assert len(root.children) == 3


def test_unranked_tree_accepts_zero_children():
    tree = ContractedUnrankedTree("a")

    assert tree.is_well_formed() is True


def test_unranked_tree_accepts_arbitrary_number_of_children():
    root = ContractedUnrankedTree("f")

    for i in range(100):
        root.add_child(ContractedUnrankedTree(str(i)))

    assert len(root.children) == 100
    assert root.is_well_formed() is True


# ---------------------------------------------------------------------------
# UnrankedTree well-formedness
# ---------------------------------------------------------------------------

def test_unranked_tree_is_well_formed():
    root = ContractedUnrankedTree("f")
    root.add_child(ContractedUnrankedTree("a"))
    root.add_child(ContractedUnrankedTree("b"))

    assert root.is_well_formed() is True


def test_unranked_tree_nested_well_formedness():
    root = ContractedUnrankedTree("f")
    child = ContractedUnrankedTree("g")
    grandchild = ContractedUnrankedTree("a")

    root.add_child(child)
    child.add_child(grandchild)

    assert root.is_well_formed() is True


# ---------------------------------------------------------------------------
# UnrankedTree rejects invalid children
# ---------------------------------------------------------------------------

def test_unranked_tree_rejects_non_tree_child():
    tree = ContractedUnrankedTree("f")

    with pytest.raises(TypeError):
        tree.add_child("a")


def test_unranked_tree_rejects_none_child():
    tree = ContractedUnrankedTree("f")

    with pytest.raises(TypeError):
        tree.add_child(None)