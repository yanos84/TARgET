import icontract

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule


class ContractedRankedFta(ranked_Fta):
    """Contracted ranked FTA used for testing."""

    @icontract.ensure(
        lambda self, fta_name="default_fta", alphabet=None,
        fta_states=None, transitions=None:
        self.name == fta_name
    )
    @icontract.ensure(
        lambda self, fta_name="default_fta", alphabet=None,
        fta_states=None, transitions=None:
        self.alphabet == alphabet
    )
    @icontract.ensure(
        lambda self, fta_name="default_fta", alphabet=None,
        fta_states=None, transitions=None:
        self.fta_states == fta_states
    )
    @icontract.ensure(
        lambda self, fta_name="default_fta", alphabet=None,
        fta_states=None, transitions=None:
        self.transitions == transitions
    )
    def __init__(
        self,
        fta_name="default_fta",
        alphabet=None,
        fta_states=None,
        transitions=None,
    ):
        super().__init__(
            fta_name=fta_name,
            alphabet=alphabet,
            fta_states=fta_states,
            transitions=transitions,
        )