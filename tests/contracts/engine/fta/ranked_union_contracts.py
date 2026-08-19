import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.union.rankedUnion import RankedFtaUnion


# ======================================================
# Helper predicates
# ======================================================

def fta_is_ranked_fta(fta):
    return isinstance(fta, ranked_Fta)


def result_is_ranked_fta(result):
    return isinstance(result, ranked_Fta)


# ======================================================
# Contracted test-only subclass
# ======================================================

class ContractedRankedFtaUnion(RankedFtaUnion):

    @icontract.require(
        lambda self: fta_is_ranked_fta(self.fta1),
        error=lambda: ViolationError(
            "fta1 must be a ranked_Fta instance"
        ),
    )
    @icontract.require(
        lambda self: fta_is_ranked_fta(self.fta2),
        error=lambda: ViolationError(
            "fta2 must be a ranked_Fta instance"
        ),
    )
    @icontract.ensure(
        result_is_ranked_fta,
        error=lambda result: ViolationError(
            f"compute must return ranked_Fta, got {type(result)}"
        ),
    )
    def compute(self):
        return super().compute()