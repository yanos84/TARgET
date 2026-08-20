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
    '''
    Test that the determinization function returns a ranked FTA.'''
    result = contracted_determinize(
        create_nondeterministic_nullary_fta,
        determinize
    )

    assert isinstance(result, ranked_Fta)


def test_determinization_combines_nullary_transitions(
    create_nondeterministic_nullary_fta
):
    '''
    Test that the determinization function combines nullary transitions
    that lead to different states into a single transition leading to a subset
    of those states.
    '''
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
    '''
    Test that the determinization function raises a ViolationError when passed an invalid FTA.'''
    with pytest.raises(icontract.ViolationError):
        contracted_determinize(None, determinize)


def test_determinization_empty_fta():
    '''
    Test that the determinization function returns an empty FTA when passed an empty FTA.'''
    automaton = ranked_Fta(
        fta_name="empty",
        alphabet=[],
        fta_states=[],
        transitions=[]
    )

    result = determinize(automaton)

    assert isinstance(result, ranked_Fta)
    assert result.transitions == []

def test_determinization_single_state():
    '''
    Test that the determinization function returns a single-state FTA when passed a single-state FTA.'''
    q0 = State(name="q0", is_Final=False)
    a = Ranked_Symbol(name="a", rank=0)

    automaton = ranked_Fta(
        fta_name="single_state",
        alphabet=[a],
        fta_states=[q0],
        transitions=[
            ranked_Rule(a, [], q0)
        ]
    )

    result = determinize(automaton)

    assert isinstance(result, ranked_Fta)
    assert len(result.transitions) == 1
    assert result.transitions[0].func.name == "a"

def test_determinization_already_deterministic():
    '''
    Test that the determinization function returns the same FTA when passed an already deterministic FTA'''
    q0 = State(name="q0", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    automaton = ranked_Fta(
        fta_name="deterministic",
        alphabet=[a, g],
        fta_states=[q0, qf],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(g, [q0], qf)
        ]
    )

    result = determinize(automaton)

    assert result==automaton

    assert len(result.transitions) == 2


def test_determinization_combines_three_nullary_destinations():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    automaton = ranked_Fta(
        fta_name="three_way_nullary",
        alphabet=[a],
        fta_states=[q0, q1, q2],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),
            ranked_Rule(a, [], q2),
        ]
    )

    result = determinize(automaton)

    a_rules = [
        rule for rule in result.transitions
        if rule.func.name == "a"
    ]

    assert len(a_rules) == 1
    assert a_rules[0].output_state.name == "{q0,q1,q2}"

def test_determinization_combines_unary_nondeterminism():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    g = Ranked_Symbol(name="g", rank=1)

    automaton = ranked_Fta(
        fta_name="unary_nondeterministic",
        alphabet=[a, g],
        fta_states=[q0, q1, q2],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(g, [q0], q1),
            ranked_Rule(g, [q0], q2),
        ]
    )

    result = determinize(automaton)

    g_rules = [
        rule for rule in result.transitions
        if rule.func.name == "g"
    ]

    assert len(g_rules) == 1
    assert g_rules[0].output_state.name == "{q1,q2}"

def test_determinization_binary_nondeterminism():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    automaton = ranked_Fta(
        fta_name="binary_nondeterministic",
        alphabet=[a, b, f],
        fta_states=[q0, q1, q2, q3],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),

            ranked_Rule(b, [], q2),
            ranked_Rule(b, [], q3),

            ranked_Rule(f, [q0, q2], q0),
            ranked_Rule(f, [q0, q3], q1),
            ranked_Rule(f, [q1, q2], q2),
            ranked_Rule(f, [q1, q3], q3),
        ]
    )

    result = determinize(automaton)

    assert isinstance(result, ranked_Fta)

def test_determinization_produces_multiple_subsets():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    automaton = ranked_Fta(
        fta_name="multiple_subsets",
        alphabet=[a, b],
        fta_states=[q0, q1, q2, q3],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),

            ranked_Rule(b, [], q2),
            ranked_Rule(b, [], q3),
        ]
    )

    result = determinize(automaton)

    a_rules = [r for r in result.transitions if r.func.name == "a"]
    b_rules = [r for r in result.transitions if r.func.name == "b"]

    assert len(a_rules) == 1
    assert len(b_rules) == 1

    assert a_rules[0].output_state.name == "{q0,q1}"
    assert b_rules[0].output_state.name == "{q2,q3}"

def test_determinization_multiple_nullary_symbols():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    automaton = ranked_Fta(
        fta_name="multiple_nullary_symbols",
        alphabet=[a, b],
        fta_states=[q0, q1, q2],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),

            ranked_Rule(b, [], q2),
        ]
    )

    result = determinize(automaton)

    a_rules = [r for r in result.transitions if r.func.name == "a"]
    b_rules = [r for r in result.transitions if r.func.name == "b"]

    assert len(a_rules) == 1
    assert len(b_rules) == 1

    assert a_rules[0].output_state.name == "{q0,q1}"
    assert b_rules[0].output_state.name == "{q2}"

def test_determinization_with_unreachable_state():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    unreachable = State(name="unreachable", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    automaton = ranked_Fta(
        fta_name="unreachable_state",
        alphabet=[a],
        fta_states=[q0, q1, unreachable],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),
        ]
    )

    result = determinize(automaton)

    assert isinstance(result, ranked_Fta)

    a_rules = [
        r for r in result.transitions
        if r.func.name == "a"
    ]

    assert len(a_rules) == 1
    assert "unreachable" not in a_rules[0].output_state.name

def test_determinization_subset_contains_final_and_nonfinal():
    q0 = State(name="q0", is_Final=True)
    q1 = State(name="q1", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    automaton = ranked_Fta(
        fta_name="mixed_finality",
        alphabet=[a],
        fta_states=[q0, q1],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q1),
        ]
    )

    result = determinize(automaton)

    a_rules = [
        r for r in result.transitions
        if r.func.name == "a"
    ]

    assert len(a_rules) == 1

    subset = a_rules[0].output_state

    assert subset.name == "{q0,q1}"
    assert subset.is_Final is True

def test_determinization_duplicate_rules():
    q0 = State(name="q0", is_Final=False)
    a = Ranked_Symbol(name="a", rank=0)

    automaton = ranked_Fta(
        fta_name="duplicate_rules",
        alphabet=[a],
        fta_states=[q0],
        transitions=[
            ranked_Rule(a, [], q0),
            ranked_Rule(a, [], q0),
        ]
    )

    result = determinize(automaton)

    a_rules = [
        r for r in result.transitions
        if r.func.name == "a"
    ]

    assert len(a_rules) == 1

def test_determinization_no_transitions():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)

    automaton = ranked_Fta(
        fta_name="no_transitions",
        alphabet=[a],
        fta_states=[q0, q1],
        transitions=[]
    )

    result = determinize(automaton)

    assert isinstance(result, ranked_Fta)
    assert result.transitions == []

def test_determinization_equivalence():
    '''
    Tests if the determinization produces equivalent automaton'''
    from TARgET.engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
    from TARgET.engine.fta.equivalence.ranked_equivalence import is_equivalent
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    random_fta = generator.generate()
    result = determinize(random_fta)

    assert is_equivalent(random_fta,result)== True
