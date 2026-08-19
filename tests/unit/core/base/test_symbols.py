import pytest

from tests.contracts.core.base.symbol_contracts import (
    ContractedSymbol,
    ContractedRankedSymbol,
)


# ---------------------------------------------------------------------------
# Symbol construction
# ---------------------------------------------------------------------------

def test_symbol_construction():
    symbol = ContractedSymbol("a")

    assert symbol.name == "a"
    assert str(symbol) == "a"


def test_symbol_empty_name():
    symbol = ContractedSymbol("")

    assert symbol.name == ""
    assert str(symbol) == ""


def test_symbol_long_name():
    name = "a" * 10_000
    symbol = ContractedSymbol(name)

    assert symbol.name == name
    assert str(symbol) == name


def test_symbol_special_characters():
    symbol = ContractedSymbol("f_1-$")

    assert symbol.name == "f_1-$"
    assert str(symbol) == "f_1-$"


# ---------------------------------------------------------------------------
# Symbol equality
# ---------------------------------------------------------------------------

def test_symbol_equal_same_name():
    s1 = ContractedSymbol("a")
    s2 = ContractedSymbol("a")

    assert s1 == s2


def test_symbol_not_equal_different_name():
    s1 = ContractedSymbol("a")
    s2 = ContractedSymbol("b")

    assert s1 != s2


def test_symbol_equality_is_symmetric():
    s1 = ContractedSymbol("a")
    s2 = ContractedSymbol("a")

    assert s1 == s2
    assert s2 == s1


@pytest.mark.parametrize(
    "other",
    [None, 1, "a", [], {}],
)
def test_symbol_not_equal_to_other_types(other):
    symbol = ContractedSymbol("a")

    assert symbol != other


# ---------------------------------------------------------------------------
# Symbol hashing
# ---------------------------------------------------------------------------

def test_equal_symbols_have_same_hash():
    s1 = ContractedSymbol("a")
    s2 = ContractedSymbol("a")

    assert s1 == s2
    assert hash(s1) == hash(s2)


def test_symbol_set_removes_duplicates():
    s1 = ContractedSymbol("a")
    s2 = ContractedSymbol("a")

    assert len({s1, s2}) == 1


def test_symbol_can_be_dictionary_key():
    symbol = ContractedSymbol("a")

    symbols = {symbol: "value"}

    assert symbols[symbol] == "value"


# ---------------------------------------------------------------------------
# Ranked_Symbol construction
# ---------------------------------------------------------------------------

def test_ranked_symbol_construction():
    symbol = ContractedRankedSymbol("a", 0)

    assert symbol.name == "a"
    assert symbol.rank == 0
    assert str(symbol) == "a"


def test_ranked_symbol_default_rank():
    symbol = ContractedRankedSymbol("a")

    assert symbol.rank == 0


def test_ranked_symbol_zero_rank():
    symbol = ContractedRankedSymbol("a", 0)

    assert symbol.rank == 0


def test_ranked_symbol_positive_rank():
    symbol = ContractedRankedSymbol("f", 3)

    assert symbol.name == "f"
    assert symbol.rank == 3


def test_ranked_symbol_large_rank():
    symbol = ContractedRankedSymbol("f", 1_000_000)

    assert symbol.rank == 1_000_000


# ---------------------------------------------------------------------------
# Ranked_Symbol equality
# ---------------------------------------------------------------------------

def test_ranked_symbols_equal_same_name_and_rank():
    s1 = ContractedRankedSymbol("f", 2)
    s2 = ContractedRankedSymbol("f", 2)

    assert s1 == s2


def test_ranked_symbols_not_equal_different_name():
    s1 = ContractedRankedSymbol("f", 2)
    s2 = ContractedRankedSymbol("g", 2)

    assert s1 != s2


def test_ranked_symbols_not_equal_different_rank():
    s1 = ContractedRankedSymbol("f", 1)
    s2 = ContractedRankedSymbol("f", 2)

    assert s1 != s2


def test_ranked_symbol_equality_is_symmetric():
    s1 = ContractedRankedSymbol("f", 2)
    s2 = ContractedRankedSymbol("f", 2)

    assert s1 == s2
    assert s2 == s1


# ---------------------------------------------------------------------------
# Symbol / Ranked_Symbol interaction
# ---------------------------------------------------------------------------

def test_symbol_and_ranked_symbol_are_not_equal():
    symbol = ContractedSymbol("f")
    ranked_symbol = ContractedRankedSymbol("f", 0)

    assert symbol != ranked_symbol
    assert ranked_symbol != symbol


def test_symbol_and_ranked_symbol_are_distinct_set_elements():
    symbol = ContractedSymbol("f")
    ranked_symbol = ContractedRankedSymbol("f", 0)

    assert len({symbol, ranked_symbol}) == 2


# ---------------------------------------------------------------------------
# Ranked_Symbol hashing
# ---------------------------------------------------------------------------

def test_equal_ranked_symbols_have_same_hash():
    s1 = ContractedRankedSymbol("f", 2)
    s2 = ContractedRankedSymbol("f", 2)

    assert s1 == s2
    assert hash(s1) == hash(s2)


def test_ranked_symbols_with_different_ranks_can_coexist_in_set():
    s1 = ContractedRankedSymbol("f", 1)
    s2 = ContractedRankedSymbol("f", 2)

    assert len({s1, s2}) == 2


def test_ranked_symbol_can_be_dictionary_key():
    symbol = ContractedRankedSymbol("f", 2)

    symbols = {symbol: "value"}

    assert symbols[symbol] == "value"


# ---------------------------------------------------------------------------
# String representation
# ---------------------------------------------------------------------------

def test_symbol_string_representation():
    assert str(ContractedSymbol("f")) == "f"


def test_ranked_symbol_string_representation():
    assert str(ContractedRankedSymbol("f", 2)) == "f"


# ---------------------------------------------------------------------------
# Manipulation
# ---------------------------------------------------------------------------

def test_symbol_name_can_be_modified():
    symbol = ContractedSymbol("a")

    symbol.name = "b"

    assert symbol.name == "b"
    assert str(symbol) == "b"


def test_ranked_symbol_name_can_be_modified():
    symbol = ContractedRankedSymbol("f", 2)

    symbol.name = "g"

    assert symbol.name == "g"
    assert symbol.rank == 2


def test_ranked_symbol_rank_can_be_modified():
    symbol = ContractedRankedSymbol("f", 2)

    symbol.rank = 3

    assert symbol.name == "f"
    assert symbol.rank == 3