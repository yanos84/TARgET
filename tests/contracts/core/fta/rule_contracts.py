import icontract

from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.state import State
from TARgET.core.base.symbol import Ranked_Symbol


class ContractedRankedRule(ranked_Rule):
    """Contracted ranked rule used for testing."""

    @icontract.ensure(
        lambda self, func, input_states=None, output_state=None,
        is_weighted=False, weight=None: self.func == func
    )
    @icontract.ensure(
        lambda self, func, input_states=None, output_state=None,
        is_weighted=False, weight=None:
        self.input_states == input_states
    )
    @icontract.ensure(
        lambda self, func, input_states=None, output_state=None,
        is_weighted=False, weight=None:
        self.output_state == output_state
    )
    @icontract.ensure(
        lambda self, func, input_states=None, output_state=None,
        is_weighted=False, weight=None:
        self.is_weighted == is_weighted
    )
    @icontract.ensure(
        lambda self, func, input_states=None, output_state=None,
        is_weighted=False, weight=None:
        self.weight == weight
    )
    def __init__(
        self,
        func: Ranked_Symbol = None,
        input_states: list[State] = None,
        output_state: State = None,
        is_weighted: bool = False,
        weight=None,
    ):
        super().__init__(
            func,
            input_states,
            output_state,
            is_weighted,
            weight,
        )