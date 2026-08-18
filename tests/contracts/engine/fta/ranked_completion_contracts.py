import icontract
from icontract import ViolationError

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.completion.ranked_completion import Completion


def fta_is_ranked_fta(self):
    return isinstance(self.fta, ranked_Fta)


def result_is_ranked_fta(result):
    return isinstance(result, ranked_Fta)


class ContractedRankedCompletion(Completion):

    @icontract.require(
        fta_is_ranked_fta,
        error=lambda self: ViolationError(
            f"FTA must be a ranked_Fta, got {type(self.fta)}"
        ),
    )
    @icontract.ensure(
        result_is_ranked_fta,
        error=lambda result: ViolationError(
            f"Completion must return a ranked_Fta, got {type(result)}"
        ),
    )
    def compute_completion(self):
        return super().compute_completion()