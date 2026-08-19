import icontract

from TARgET.core.algebraic.trop_semiring import TropicalSemiring


class ContractedTropicalSemiring(TropicalSemiring):

    @icontract.ensure(
        lambda self, value: self.value == float(value)
    )
    def __init__(self, value: float):
        super().__init__(value)