import pytest
import icontract

from tests.contracts.engine.fta.acceptor_contracts import (
    ContractedRankedBottomUpAcceptor as RA
)

from core.symbol import Ranked_Symbol
from fta.rankedRule import ranked_Rule
from fta.rankedfta import ranked_Fta
from core.rankedTree import RankedTree
from fta.state import State


@pytest.fixture
def create_fta():
    s = State(name="q1", is_Final=False)
    t = State(name="q2", is_Final=False)
    u = State(name="q3", is_Final=True)

    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    rules = [
        ranked_Rule(f, [s, t], u),
        ranked_Rule(a, [], s),
        ranked_Rule(b, [], t)
    ]

    automaton = ranked_Fta(
        fta_name="fta1",
        alphabet=[f, a, b],
        fta_states=[s, t, u],
        transitions=rules
    )

    root = RankedTree(symbol=f)
    root.add_child(RankedTree(symbol=a))
    root.add_child(RankedTree(symbol=b))

    return automaton, root


def test_ranked_acceptor_accepts(create_fta):
    acceptor = RA()
    automaton, root = create_fta
    assert acceptor.accepts(automaton, root) is True


def test_acceptor_rejects_none_tree(create_fta):
    acceptor = RA()
    automaton, _ = create_fta

    with pytest.raises(icontract.ViolationError):
        acceptor.accepts(automaton, None)


def test_acceptor_invariant():
    acceptor = RA()
    assert callable(getattr(acceptor, "_compute_states", None))
