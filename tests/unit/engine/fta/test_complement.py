from fta.rankedfta import ranked_Fta
from fta.state import State
from core.symbol import Ranked_Symbol

from tests.contracts.engine.fta.complement_contracts import ContractedComplement


def test_complement_flips_final_states():
    # States
    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)

    # Alphabet
    f = Ranked_Symbol("f", rank=1)

    # Dummy FTA (minimal structure)
    fta = ranked_Fta(
        alphabet=[f],
        fta_states={q0, q1},
        transitions=[]
    )

    complement = ContractedComplement(fta)
    comp_fta = complement.compute_complement()

    # Finality must be flipped
    assert q0.is_Final is False  # original untouched
    assert q1.is_Final is True

    comp_states = {s.name: s for s in comp_fta.fta_states}
    assert comp_states["q0"].is_Final is True
    assert comp_states["q1"].is_Final is False
