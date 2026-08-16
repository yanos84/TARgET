import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.product.ranked_prod import Ranked_prod


# ======================================================
# Helper predicates
# ======================================================

def fta1_is_ranked_fta(fta1):
    return isinstance(fta1, ranked_Fta)


def fta2_is_ranked_fta(fta2):
    return isinstance(fta2, ranked_Fta)


def result_is_ranked_fta(result):
    return isinstance(result, ranked_Fta)


# ======================================================
# Contracted test-only subclass
# ======================================================

class ContractedRankedProd(Ranked_prod):

    @icontract.require(
        fta1_is_ranked_fta,
        error=lambda fta1: ViolationError(
            f"First FTA must be a ranked_Fta, got {type(fta1)}"
        ),
    )
    @icontract.require(
        fta2_is_ranked_fta,
        error=lambda fta2: ViolationError(
            f"Second FTA must be a ranked_Fta, got {type(fta2)}"
        ),
    )
    @icontract.ensure(
        result_is_ranked_fta,
        error=lambda result: ViolationError(
            f"product must return ranked_Fta, got {type(result)}"
        ),
    )
    def product(self, fta1, fta2):
        return super().product(fta1, fta2)