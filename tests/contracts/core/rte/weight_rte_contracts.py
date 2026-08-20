import icontract

from TARgET.core.rte.rte import Rte
from TARgET.core.rte.weighted.weight import Weight
from TARgET.core.algebraic.semiring import Semiring


class ContractedWeight(Weight):
    """Contracted weighted RTE used for testing."""

    @icontract.ensure(
        lambda self, weight, expr: self.weight == weight
    )
    @icontract.ensure(
        lambda self, weight, expr: self.expr == expr
    )
    def __init__(self, weight: Semiring, expr: Rte):
        super().__init__(weight, expr)