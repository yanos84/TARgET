import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.difference.ranked_diff import Ranked_Diff


# ======================================================
# Helper predicates
# ======================================================

def ftas_are_ranked_fta(fta1, fta2):
    return (
        isinstance(fta1, ranked_Fta)
        and isinstance(fta2, ranked_Fta)
    )


def result_is_ranked_fta(result):
    return isinstance(result, ranked_Fta)


def result_is_bool(result):
    return isinstance(result, bool)


# ======================================================
# Contracted test-only subclass
# ======================================================

class ContractedRankedDiff(Ranked_Diff):

    @icontract.require(
        ftas_are_ranked_fta,
        error=lambda fta1, fta2: ViolationError(
            "fta1 and fta2 must both be ranked_Fta instances"
        ),
    )
    @icontract.ensure(
        result_is_ranked_fta,
        error=lambda result: ViolationError(
            f"diff must return a ranked_Fta, got {type(result)}"
        ),
    )
    def diff(self, fta1, fta2):
        return super().diff(fta1, fta2)

    @icontract.require(
        ftas_are_ranked_fta,
        error=lambda fta1, fta2: ViolationError(
            "fta1 and fta2 must both be ranked_Fta instances"
        ),
    )
    @icontract.ensure(
        result_is_bool,
        error=lambda result: ViolationError(
            f"is_equivalent must return bool, got {type(result)}"
        ),
    )
    def is_equivalent(self, fta1, fta2):
        return super().is_equivalent(fta1, fta2)