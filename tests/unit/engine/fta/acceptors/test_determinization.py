import pytest
import icontract

from tests.contracts.engine.fta.determinization_contracts import (
    contracted_determinize
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.engine.fta.determinization.ranked_determinization import determinize

#from TARgET.engine.fta.determinization import determinize


@pytest.fixture
def create_nondeterministic_nullary_fta():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rules = [
        # a() -> q0
        ranked_Rule(a, [], q0),

        # a() -> q1
        ranked_Rule(a, [], q1)
    ]

    automaton = ranked_Fta(
        fta_name="nondeterministic_nullary_fta",
        alphabet=[a],
        fta_states=[q0, q1],
        transitions=rules
    )

    return automaton


def test_determinization_returns_ranked_fta(
    create_nondeterministic_nullary_fta
):
    result = contracted_determinize(
        create_nondeterministic_nullary_fta,
        determinize
    )

    assert isinstance(result, ranked_Fta)


def test_determinization_combines_nullary_transitions(
    create_nondeterministic_nullary_fta
):
    determ_fta = determinize(create_nondeterministic_nullary_fta)

    a_rules = [
        rule
        for rule in determ_fta.transitions
        if rule.func.name == "a"
    ]

    # There must be exactly one deterministic transition for a().
    assert len(a_rules) == 1

    # Its destination must be the subset {q0,q1}.
    assert a_rules[0].output_state.name == "{q0,q1}"


def test_determinization_rejects_invalid_fta():
    with pytest.raises(icontract.ViolationError):
        contracted_determinize(None, determinize)