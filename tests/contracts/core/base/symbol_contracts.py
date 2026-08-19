import icontract

from TARgET.core.base.symbol import Symbol, Ranked_Symbol


class ContractedSymbol(Symbol):
    """Contracted version of Symbol for testing."""

    @icontract.ensure(
        lambda self, name: self.name == name
    )
    @icontract.ensure(
        lambda self: str(self) == self.name
    )
    def __init__(self, name: str):
        super().__init__(name)


class ContractedRankedSymbol(Ranked_Symbol):
    """Contracted version of Ranked_Symbol for testing."""

    @icontract.ensure(
        lambda self, name, rank=0: self.name == name
    )
    @icontract.ensure(
        lambda self, name, rank=0: self.rank == rank
    )
    @icontract.ensure(
        lambda self: str(self) == self.name
    )
    def __init__(self, name: str, rank: int = 0):
        super().__init__(name, rank)