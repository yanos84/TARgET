import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta



# ======================================================
# Helper predicates
# ======================================================

def fta_is_ranked_fta(fta):
    return isinstance(fta, ranked_Fta)


def result_is_ranked_fta(result):
    return isinstance(result, ranked_Fta)


# ======================================================
# Contracted test-only wrapper
# ======================================================

@icontract.require(
    fta_is_ranked_fta,
    error=lambda fta: ViolationError(
        f"FTA must be a ranked_Fta, got {type(fta)}"
    ),
)
@icontract.ensure(
    result_is_ranked_fta,
    error=lambda result: ViolationError(
        f"determinize must return ranked_Fta, got {type(result)}"
    ),
)
def contracted_determinize(fta, determinize_function):
    return determinize_function(fta)