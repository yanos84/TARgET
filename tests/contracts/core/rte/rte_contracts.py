import icontract

from TARgET.core.rte.rte import (
    Zero,
    One,
    Atom,
    function,
    Plus,
    CProduct,
    CStar,
)


class ContractedZero(Zero):
    """Contracted Zero RTE used for testing."""

    @icontract.ensure(
        lambda self: str(self) == "0"
    )
    def __init__(self):
        super().__init__()


class ContractedOne(One):
    """Contracted One RTE used for testing."""

    @icontract.ensure(
        lambda self: str(self) == "1"
    )
    def __init__(self):
        super().__init__()


class ContractedAtom(Atom):
    """Contracted Atom RTE used for testing."""

    @icontract.ensure(
        lambda self, symbol: self.symbol == symbol
    )
    def __init__(self, symbol):
        super().__init__(symbol)


class ContractedFunction(function):
    """Contracted function RTE used for testing."""

    @icontract.ensure(
        lambda self, symbol, args:
        self.symbol == symbol
    )
    @icontract.ensure(
        lambda self, symbol, args:
        self.args is not None
    )
    def __init__(self, symbol, args=None):
        super().__init__(symbol, args)


class ContractedPlus(Plus):
    """Contracted Plus RTE used for testing."""

    @icontract.ensure(
        lambda self:
        len(self.terms) == len(set(self.terms))
    )
    @icontract.ensure(
        lambda self:
        all(not isinstance(term, Plus) for term in self.terms)
    )
    def __init__(self, *terms):
        super().__init__(*terms)


class ContractedCProduct(CProduct):
    """Contracted CProduct RTE used for testing."""

    @icontract.ensure(
        lambda self, left, right, concat:
        self.left == left
    )
    @icontract.ensure(
        lambda self, left, right, concat:
        self.right == right
    )
    @icontract.ensure(
        lambda self, left, right, concat:
        self.concat == concat
    )
    def __init__(self, left, right, concat):
        super().__init__(left, right, concat)


class ContractedCStar(CStar):
    """Contracted CStar RTE used for testing."""

    @icontract.ensure(
        lambda self, expr, concat:
        self.expr == expr
    )
    @icontract.ensure(
        lambda self, expr, concat:
        self.concat == concat
    )
    def __init__(self, expr, concat):
        super().__init__(expr, concat)