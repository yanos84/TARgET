import icontract

from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.useless_dropping.drop_useless_states_bottomUpFta import (
    productive_states,
    reachable_states,
    drop_useless_states,
)


class ContractedUselessStates:

    @icontract.require(
        lambda fta: isinstance(fta, ranked_Fta),
        "fta must be a ranked_Fta instance",
    )
    def productive_states(self, fta):
        return productive_states(fta)

    @icontract.require(
        lambda fta: isinstance(fta, ranked_Fta),
        "fta must be a ranked_Fta instance",
    )
    def reachable_states(self, fta):
        return reachable_states(fta)

    @icontract.require(
        lambda fta: isinstance(fta, ranked_Fta),
        "fta must be a ranked_Fta instance",
    )
    @icontract.ensure(
        lambda result: isinstance(result, ranked_Fta),
        "result must be a ranked_Fta instance",
    )
    def drop_useless_states(self, fta):
        return drop_useless_states(fta)