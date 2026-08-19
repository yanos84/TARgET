import icontract

from TARgET.core.algebraic.integer_semiring import IntegerSemiring


class ContractedIntegerSemiring(IntegerSemiring):

    @icontract.ensure(
        lambda self, value: self.value == int(value)
    )
    def __init__(self, value: int):
        super().__init__(value)