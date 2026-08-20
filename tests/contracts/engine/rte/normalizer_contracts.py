import icontract

from TARgET.core.rte.rte import Rte
from TARgET.engine.rte.normalize.normalize import Normalizer


class ContractedNormalizer(Normalizer):
    """Contracted RTE normalizer used for testing."""

    @icontract.ensure(
        lambda self, expr, result: isinstance(result, Rte)
    )
    def normalize(self, expr: Rte) -> Rte:
        return super().normalize(expr)