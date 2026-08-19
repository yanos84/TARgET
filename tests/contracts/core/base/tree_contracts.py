import icontract

from TARgET.core.base.tree import AbstractTree
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.base.unrankedTree import UnrankedTree
from TARgET.core.base.symbol import Ranked_Symbol


class ContractedTree(AbstractTree):
    """Concrete contracted tree used to test AbstractTree behavior."""

    @icontract.ensure(
        lambda self, symbol: self.symbol == symbol
    )
    def __init__(self, symbol: str):
        super().__init__(symbol)

    def is_well_formed(self) -> bool:
        return all(child.is_well_formed() for child in self.children)


class ContractedRankedTree(RankedTree):
    """Contracted RankedTree used for testing."""

    @icontract.ensure(
        lambda self, symbol: self.ranked_symbol == symbol
    )
    @icontract.ensure(
        lambda self: self.symbol == self.ranked_symbol.name
    )
    def __init__(self, symbol: Ranked_Symbol):
        super().__init__(symbol)


class ContractedUnrankedTree(UnrankedTree):
    """Contracted UnrankedTree used for testing."""

    @icontract.ensure(
        lambda self, symbol: self.symbol == symbol
    )
    def __init__(self, symbol: str):
        super().__init__(symbol)