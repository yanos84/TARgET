import copy
import icontract

from TARgET.core.fta.abst_fta import Fta
from TARgET.core.base.symbol import Symbol
from TARgET.engine.fta.complement.complement import Complement


class ContractedComplement(Complement):

    @icontract.require(
        lambda self: hasattr(self, "fta") and isinstance(self.fta, Fta),
        error=ValueError("Complement must have a valid Fta")
    )
    @icontract.require(
        lambda self: (
            hasattr(self.fta, "alphabet")
            and isinstance(self.fta.alphabet, list)
            and all(isinstance(sym, Symbol) for sym in self.fta.alphabet)
        ),
        error=TypeError("Alphabet must be a list of Symbol instances")
    )
    @icontract.snapshot(
        lambda self: copy.deepcopy(self.fta),
        name="fta_before"
    )
    @icontract.ensure(
        lambda self, OLD: self.fta is not OLD.fta_before,
        error=RuntimeError("compute_complement must not mutate the original Fta")
    )
    def compute_complement(self) -> Fta:
        return super().compute_complement()

