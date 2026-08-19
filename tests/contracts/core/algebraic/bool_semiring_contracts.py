import icontract

from TARgET.core.algebraic.bool_semiring import BooleanSemiring


class ContractedBooleanSemiring(BooleanSemiring):
    """Contracted Boolean semiring used for testing."""

    @icontract.ensure(
        lambda self, value: self.value is bool(value)
    )
    def __init__(self, value: bool):
        super().__init__(value)