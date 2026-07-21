import copy
import icontract

from TARgET.core.fta.abst_fta import Fta
from TARgET.core.base.symbol import Symbol


class ContractedComplement:
    """
    Complement of a finite tree automaton (FTA),
    with method-level contracts only (Python 3.13 safe).
    """

    def __init__(self, fta: Fta) -> None:
        self.fta = copy.deepcopy(fta)

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
        """
        Compute the complement of the FTA
        by flipping final and non-final states.
        """

        for state in self.fta.fta_states:
            state.is_Final = not state.is_Final

        for transition in self.fta.transitions:
            for s in transition.input_states:
                s.is_Final = not s.is_Final
            transition.output_state.is_Final = not s.is_Final

        return self.fta
