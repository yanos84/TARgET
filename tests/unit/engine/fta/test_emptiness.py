import pytest
import icontract

from tests.contracts.engine.fta.emptiness_contracts import (
    ContractedRankedEmptiness as RE
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


@pytest.fixture
def create_non_empty_fta():
    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    rules = [
        # a() -> q0
        ranked_Rule(a, [], q0),

        # g(q0) -> qf
        ranked_Rule(g, [q0], qf)
    ]

    automaton = ranked_Fta(
        fta_name="non_empty_fta",
        alphabet=[a, g],
        fta_states=[q0, qf],
        transitions=rules
    )

    return automaton


def test_emptiness_non_empty_nested_tree(create_non_empty_fta):
    emptiness_checker = RE()

    assert emptiness_checker.is_empty(create_non_empty_fta) is False


def test_emptiness_rejects_invalid_fta():
    emptiness_checker = RE()

    with pytest.raises(icontract.ViolationError):
        emptiness_checker.is_empty(None)