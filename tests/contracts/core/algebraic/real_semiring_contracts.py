import icontract

from TARgET.core.algebraic.real_semiring import RealSemiring


class ContractedRealSemiring(RealSemiring):

    @icontract.ensure(
        lambda self, value: self.value == float(value)
    )
    def __init__(self, value: float):
        super().__init__(value)