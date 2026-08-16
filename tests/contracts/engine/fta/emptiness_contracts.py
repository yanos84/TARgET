import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.emptiness.ranked_emptiness import RankedEmptiness


# ======================================================
# Helper predicates
# ======================================================

def fta_is_ranked_fta(fta):
    return isinstance(fta, ranked_Fta)


def result_is_bool(result):
    return isinstance(result, bool)


# ======================================================
# Contracted test-only subclass
# ======================================================

class ContractedRankedEmptiness(RankedEmptiness):

    @icontract.require(
        fta_is_ranked_fta,
        error=lambda fta: ViolationError(
            f"FTA must be a ranked_Fta, got {type(fta)}"
        ),
    )
    @icontract.ensure(
        result_is_bool,
        error=lambda result: ViolationError(
            f"is_empty must return bool, got {type(result)}"
        ),
    )
    def is_empty(self, fta):
        return super().is_empty(fta)