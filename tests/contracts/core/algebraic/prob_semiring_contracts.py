import icontract

from TARgET.core.algebraic.stochastic_semiring import ProbabilitySemiring


class ContractedProbabilitySemiring(ProbabilitySemiring):

    @icontract.ensure(
        lambda self, value: self.value == float(value)
    )
    def __init__(self, value: float):
        super().__init__(value)