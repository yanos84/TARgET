from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.core.base.symbol import Ranked_Symbol

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
        fta_states=[q0, q1],
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

def test_complement_does_not_modify_original():
    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)

    a = Ranked_Symbol("a", rank=0)

    fta = ranked_Fta(
        alphabet=[a],
        fta_states=[q0, q1],
        transitions=[]
    )

    complement = ContractedComplement(fta)
    comp_fta = complement.compute_complement()

    assert q0.is_Final is False
    assert q1.is_Final is True

    assert comp_fta is not fta

def test_complement_empty_language():
    q0 = State("q0", is_Final=False)

    a = Ranked_Symbol("a", rank=0)

    fta = ranked_Fta(
        fta_name="empty_language",
        alphabet=[a],
        fta_states=[q0],
        transitions=[
            # whatever transition representation your ranked_Fta expects
        ]
    )

    comp_fta = ContractedComplement(fta).compute_complement()

    comp_states = {s.name: s for s in comp_fta.fta_states}

    assert comp_states["q0"].is_Final is True

def test_complement_completes_fta():
    q0 = State("q0", is_Final=True)

    a = Ranked_Symbol("a", rank=0)
    f = Ranked_Symbol("f", rank=1)

    fta = ranked_Fta(
        alphabet=[a, f],
        fta_states=[q0],
        transitions=[]
    )

    comp_fta = ContractedComplement(fta).compute_complement()

    # Original FTA must remain unchanged
    assert [s.name for s in fta.fta_states] == ["q0"]

    # Completion introduces a sink state
    comp_state_names = {s.name for s in comp_fta.fta_states}

    assert "q0" in comp_state_names
    assert "sink" in comp_state_names

    # The sink is non-final before complement and therefore
    # final after complement.
    sink = next(
        s for s in comp_fta.fta_states
        if s.name == "sink"
    )

    assert sink.is_Final is True

def test_complement_equality_two_equal_fta():
    from TARgET.core.fta.rankedRule import ranked_Rule
    a = Ranked_Symbol("a", 0)
    f = Ranked_Symbol("f", 1)

    q0 = State("q0", is_Final=False)
    q1 = State("q1", is_Final=True)

    r0 = State("r0", is_Final=False)
    r1 = State("r1", is_Final=True)

    rule1 = ranked_Rule(func=a)
    rule1.input_states = []
    rule1.output_state = q0

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [q0]
    rule2.output_state = q1

    rule3 = ranked_Rule(func=a)
    rule3.input_states = []
    rule3.output_state = r0

    rule4 = ranked_Rule(func=f)
    rule4.input_states = [r0]
    rule4.output_state = r1

    fta1 = ranked_Fta(
        fta_name="fta1",
        alphabet=[a, f],
        fta_states=[q0, q1],
        transitions=[rule1, rule2],
    )

    fta2 = ranked_Fta(
        fta_name="fta2",
        alphabet=[a, f],
        fta_states=[r0, r1],
        transitions=[rule3, rule4],
    )
    complement1 = ContractedComplement(fta1).compute_complement()
    complement2 = ContractedComplement(fta2).compute_complement()
    assert complement1 == complement2