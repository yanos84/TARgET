import icontract

from TARgET.core.fta.abst_fta import Fta
from TARgET.engine.fta.minimization.dfta_standard_minimization import dfta_minimizer


class ContractedMinimizer(dfta_minimizer):
    """
    Contracted version of dfta_minimizer.

    Contracts are placed on the public minimize method while the
    actual minimization algorithm is inherited from dfta_minimizer.
    """

    @icontract.require(
        lambda self, fta: isinstance(fta, Fta),
        error=TypeError("Minimization requires a valid Fta")
    )
    @icontract.require(
        lambda self, fta: self.check_determinism(fta),
        error=ValueError(
            "FTA must be deterministic for minimization."
        )
    )
    @icontract.snapshot(
        lambda self, fta: len(fta.fta_states),
        name="state_count_before"
    )
    @icontract.ensure(
        lambda result: isinstance(result, Fta),
        error=TypeError(
            "Minimization must return an Fta"
        )
    )
    @icontract.ensure(
        lambda self, fta, result:
            len(result.fta_states) <= len(fta.fta_states),
        error=AssertionError(
            "Minimized FTA must not have more states than the original"
        )
    )
    def minimize(self, fta):
        return super().minimize(fta)