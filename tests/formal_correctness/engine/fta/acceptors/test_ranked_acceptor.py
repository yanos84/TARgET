import pytest
from engine.fta.acceptors.rankedAcceptor import RankedBottomUpAcceptor as RA
from core.symbol import Ranked_Symbol
from fta.rankedRule import ranked_Rule
from fta.rankedfta import ranked_Fta
from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
from core.rankedTree import RankedTree
from fta.state import State
import deal


@pytest.fixture
def create_fta():
    """Creates an fta for test"""
    s= State(name="q1", is_Final=False)
    t=State(name="q2", is_Final=False)
    u=State(name="q3", is_Final=True)
    st = []
    st.append(s)
    st.append(t)
    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    rule = ranked_Rule(func = f)
    rule.input_states = st
    rule.output_state = u
    rules = []
    rules.append(rule)
    #rules.append(rule)
    rules.append(ranked_Rule(a, [], s))
    rules.append(ranked_Rule(b, [], t))
    alpha = []
    alpha.append(f)
    alpha.append(a)
    alpha.append(b)
    automaton = ranked_Fta(fta_name="fta1", alphabet=alpha, fta_states=st, transitions=rules)
    automaton.print_Fta()

    root = RankedTree(symbol=f)
    child1 = RankedTree(symbol=a)
    child2 = RankedTree(symbol=b)
    root.add_child(child1)
    root.add_child(child2)
    return automaton, root

def test_ranked_acceptor(create_fta):
    acceptor = RA()
    automaton, root = create_fta
    assert acceptor.accepts(automaton, root) == True
