import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.product.ranked_prod import Ranked_prod


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


# ======================================================
# Contracted test-only subclass
# ======================================================

class ContractedRankedProd(Ranked_prod):

    @icontract.require(
        ftas_are_ranked_fta,
        error=lambda fta1, fta2: ViolationError(
            "fta1 and fta2 must both be ranked_Fta instances"
        ),
    )
    @icontract.ensure(
        result_is_ranked_fta,
        error=lambda result: ViolationError(
            f"product must return a ranked_Fta, got {type(result)}"
        ),
    )
    def product(self, fta1, fta2):
        return super().product(fta1, fta2)