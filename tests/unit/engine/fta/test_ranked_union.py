import pytest
import icontract

from tests.contracts.engine.fta.ranked_union_contracts import (
    ContractedRankedFtaUnion as RU
)

from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State


# ======================================================
# Helpers
# ======================================================

def make_rule(symbol, inputs, output):
    return ranked_Rule(
        symbol,
        inputs,
        output
    )


def make_fta(name, states, alphabet, transitions):
    return ranked_Fta(
        fta_name=name,
        alphabet=alphabet,
        fta_states=states,
        transitions=transitions
    )


# ======================================================
# Test 1
# Disjoint alphabets
#
# FTA1:
#   a() -> qf
#
# FTA2:
#   b() -> pf
#
# Expected:
#   alphabet = {a, b}
#   both transitions preserved
#   both final states preserved
# ======================================================

@pytest.fixture
def create_disjoint_alphabet_fta():

    qf = State(name="qf", is_Final=True)
    pf = State(name="pf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [qf],
        [a],
        [make_rule(a, [], qf)]
    )

    fta2 = make_fta(
        "fta2",
        [pf],
        [b],
        [make_rule(b, [], pf)]
    )

    return fta1, fta2


def test_union_disjoint_alphabets(create_disjoint_alphabet_fta):

    fta1, fta2 = create_disjoint_alphabet_fta

    union = RU(fta1, fta2).compute()

    assert len(union.alphabet) == 2
    assert {symbol.name for symbol in union.alphabet} == {"a", "b"}

    assert len(union.transitions) == 2

    assert {
        rule.func.name
        for rule in union.transitions
    } == {"a", "b"}

    assert all(
        rule.output_state.is_Final
        for rule in union.transitions
    )


# ======================================================
# Test 2
# Same alphabet
#
# FTA1:
#   a() -> q1
#
# FTA2:
#   a() -> p1
#
# Expected:
#   only one alphabet symbol
#   both transitions preserved
# ======================================================

def test_union_same_alphabet():

    q1 = State(name="q1", is_Final=True)
    p1 = State(name="p1", is_Final=True)

    a1 = Ranked_Symbol(name="a", rank=0)
    a2 = Ranked_Symbol(name="a", rank=0)

    fta1 = make_fta(
        "fta1",
        [q1],
        [a1],
        [make_rule(a1, [], q1)]
    )

    fta2 = make_fta(
        "fta2",
        [p1],
        [a2],
        [make_rule(a2, [], p1)]
    )

    union = RU(fta1, fta2).compute()

    assert len(union.alphabet) == 1
    assert union.alphabet[0].name == "a"
    assert union.alphabet[0].rank == 0

    assert len(union.transitions) == 2


# ======================================================
# Test 3
# Conflicting state names
#
# FTA1:
#   a() -> q
#
# FTA2:
#   b() -> q
#
# The second q must be renamed to 2_q.
# ======================================================

def test_union_renames_conflicting_states():

    q1 = State(name="q", is_Final=True)
    q2 = State(name="q", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [q1],
        [a],
        [make_rule(a, [], q1)]
    )

    fta2 = make_fta(
        "fta2",
        [q2],
        [b],
        [make_rule(b, [], q2)]
    )

    union = RU(fta1, fta2).compute()

    state_names = {
        state.name
        for state in union.fta_states
    }

    assert state_names == {"q", "2_q"}

    transition_outputs = {
        rule.output_state.name
        for rule in union.transitions
    }

    assert transition_outputs == {"q", "2_q"}


# ======================================================
# Test 4
# Multiple conflicting states
#
# q1 and q2 occur in both automata.
#
# Expected:
#   q1, q2, 2_q1, 2_q2
# ======================================================

def test_union_multiple_conflicting_states():

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=True)

    p1 = State(name="q1", is_Final=True)
    p2 = State(name="q2", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [q1, q2],
        [a],
        [
            make_rule(a, [], q1),
            make_rule(a, [], q2),
        ]
    )

    fta2 = make_fta(
        "fta2",
        [p1, p2],
        [b],
        [
            make_rule(b, [], p1),
            make_rule(b, [], p2),
        ]
    )

    union = RU(fta1, fta2).compute()

    assert {
        state.name
        for state in union.fta_states
    } == {
        "q1",
        "q2",
        "2_q1",
        "2_q2"
    }


# ======================================================
# Test 5
# No state-name conflicts
#
# Expected:
#   states remain unchanged.
# ======================================================

def test_union_no_state_conflicts():

    q = State(name="q", is_Final=True)
    p = State(name="p", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [q],
        [a],
        [make_rule(a, [], q)]
    )

    fta2 = make_fta(
        "fta2",
        [p],
        [b],
        [make_rule(b, [], p)]
    )

    union = RU(fta1, fta2).compute()

    assert {
        state.name
        for state in union.fta_states
    } == {"q", "p"}


# ======================================================
# Test 6
# Final-state preservation
#
# FTA1:
#   a() -> qf       qf final
#
# FTA2:
#   b() -> p        p not final
#
# Expected:
#   qf remains final
#   p remains non-final
# ======================================================

def test_union_final_state_preservation():

    qf = State(name="qf", is_Final=True)
    p = State(name="p", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [qf],
        [a],
        [make_rule(a, [], qf)]
    )

    fta2 = make_fta(
        "fta2",
        [p],
        [b],
        [make_rule(b, [], p)]
    )

    union = RU(fta1, fta2).compute()

    states = {
        state.name: state
        for state in union.fta_states
    }

    assert states["qf"].is_Final is True
    assert states["p"].is_Final is False


# ======================================================
# Test 7
# Final-state conflict
#
# Both states are named q but have different final flags.
#
# FTA1:
#   a() -> q       final
#
# FTA2:
#   b() -> q       non-final
#
# Expected:
#   q     -> final
#   2_q   -> non-final
# ======================================================

def test_union_conflicting_states_preserve_final_flags():

    q1 = State(name="q", is_Final=True)
    q2 = State(name="q", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [q1],
        [a],
        [make_rule(a, [], q1)]
    )

    fta2 = make_fta(
        "fta2",
        [q2],
        [b],
        [make_rule(b, [], q2)]
    )

    union = RU(fta1, fta2).compute()

    states = {
        state.name: state
        for state in union.fta_states
    }

    assert states["q"].is_Final is True
    assert states["2_q"].is_Final is False


# ======================================================
# Test 8
# Nullary and unary transitions
#
# FTA1:
#   a() -> q
#   f(q) -> qf
#
# FTA2:
#   b() -> p
#   f(p) -> pf
#
# Expected:
#   all four transitions are preserved.
# ======================================================

def test_union_nullary_and_unary_transitions():

    q = State(name="q", is_Final=False)
    qf = State(name="qf", is_Final=True)

    p = State(name="p", is_Final=False)
    pf = State(name="pf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f1 = Ranked_Symbol(name="f", rank=1)
    f2 = Ranked_Symbol(name="f", rank=1)

    fta1 = make_fta(
        "fta1",
        [q, qf],
        [a, f1],
        [
            make_rule(a, [], q),
            make_rule(f1, [q], qf),
        ]
    )

    fta2 = make_fta(
        "fta2",
        [p, pf],
        [b, f2],
        [
            make_rule(b, [], p),
            make_rule(f2, [p], pf),
        ]
    )

    union = RU(fta1, fta2).compute()

    assert len(union.transitions) == 4

    assert {
        rule.func.name
        for rule in union.transitions
    } == {"a", "b", "f"}


# ======================================================
# Test 9
# Binary transitions
#
# Verify that child states are correctly renamed.
# ======================================================

def test_union_binary_transitions_with_conflicting_states():

    q = State(name="q", is_Final=False)
    qf = State(name="qf", is_Final=True)

    p = State(name="q", is_Final=False)
    pf = State(name="pf", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    fta1 = make_fta(
        "fta1",
        [q, qf],
        [a, f],
        [
            make_rule(a, [], q),
            make_rule(f, [q, q], qf),
        ]
    )

    fta2 = make_fta(
        "fta2",
        [p, pf],
        [a, f],
        [
            make_rule(a, [], p),
            make_rule(f, [p, p], pf),
        ]
    )

    union = RU(fta1, fta2).compute()

    assert len(union.transitions) == 4

    transition_names = {
        (
            rule.func.name,
            tuple(state.name for state in rule.input_states),
            rule.output_state.name,
        )
        for rule in union.transitions
    }

    assert (
        "f",
        ("q", "q"),
        "qf"
    ) in transition_names

    assert (
        "f",
        ("2_q", "2_q"),
        "pf"
    ) in transition_names


# ======================================================
# Test 10
# Empty FTA + non-empty FTA
#
# FTA1 accepts nothing.
# FTA2 accepts {a}.
#
# Expected:
#   union accepts exactly what FTA2 accepts.
# ======================================================

def test_union_empty_and_non_empty():

    a = Ranked_Symbol(name="a", rank=0)

    empty_state = State(name="empty", is_Final=False)

    p = State(name="p", is_Final=True)

    empty_fta = make_fta(
        "empty",
        [empty_state],
        [a],
        []
    )

    non_empty_fta = make_fta(
        "non_empty",
        [p],
        [a],
        [make_rule(a, [], p)]
    )

    union = RU(empty_fta, non_empty_fta).compute()

    assert len(union.transitions) == 1

    final_outputs = [
        rule.output_state
        for rule in union.transitions
        if rule.output_state.is_Final
    ]

    assert len(final_outputs) == 1
    assert final_outputs[0].name == "p"


# ======================================================
# Test 11
# Both FTAs empty
#
# Expected:
#   no transitions.
# ======================================================

def test_union_two_empty_automata():

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    q = State(name="q", is_Final=False)
    p = State(name="p", is_Final=False)

    fta1 = make_fta(
        "empty1",
        [q],
        [a],
        []
    )

    fta2 = make_fta(
        "empty2",
        [p],
        [b],
        []
    )

    union = RU(fta1, fta2).compute()

    assert len(union.transitions) == 0
    assert len(union.fta_states) == 2
    assert len(union.alphabet) == 2


# ======================================================
# Test 12
# Duplicate transitions
#
# Same transition occurs twice in FTA1.
#
# RankedFtaUnion uses a set, so duplicate transitions
# should collapse.
# ======================================================

def test_union_duplicate_transitions():

    q = State(name="q", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)

    r1 = make_rule(a, [], q)
    r2 = make_rule(a, [], q)

    fta1 = make_fta(
        "fta1",
        [q],
        [a],
        [r1, r2]
    )

    p = State(name="p", is_Final=True)

    b = Ranked_Symbol(name="b", rank=0)

    fta2 = make_fta(
        "fta2",
        [p],
        [b],
        [make_rule(b, [], p)]
    )

    union = RU(fta1, fta2).compute()

    a_transitions = [
        rule
        for rule in union.transitions
        if rule.func.name == "a"
    ]

    assert len(a_transitions) == 1


# ======================================================
# Test 13
# Different ranks with same symbol name
#
# Both alphabets contain f, but with different ranks.
#
# They are different ranked symbols and must both remain.
# ======================================================

def test_union_same_symbol_name_different_rank():

    q = State(name="q", is_Final=True)
    p = State(name="p", is_Final=True)

    f1 = Ranked_Symbol(name="f", rank=1)
    f2 = Ranked_Symbol(name="f", rank=2)

    x = State(name="x", is_Final=False)
    y = State(name="y", is_Final=False)

    fta1 = make_fta(
        "fta1",
        [x, q],
        [f1],
        [make_rule(f1, [x], q)]
    )

    fta2 = make_fta(
        "fta2",
        [y, p],
        [f2],
        [make_rule(f2, [y, y], p)]
    )

    union = RU(fta1, fta2).compute()

    assert len(union.alphabet) == 2

    ranks = {
        symbol.rank
        for symbol in union.alphabet
        if symbol.name == "f"
    }

    assert ranks == {1, 2}

    assert len(union.transitions) == 2


# ======================================================
# Test 14
# Initial-state preservation
#
# Verify that is_Initial survives state renaming.
# ======================================================

def test_union_initial_state_preservation():

    q = State(
        name="q",
        is_Final=True,
        is_Initial=True
    )

    p = State(
        name="q",
        is_Final=False,
        is_Initial=True
    )

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)

    fta1 = make_fta(
        "fta1",
        [q],
        [a],
        [make_rule(a, [], q)]
    )

    fta2 = make_fta(
        "fta2",
        [p],
        [b],
        [make_rule(b, [], p)]
    )

    union = RU(fta1, fta2).compute()

    states = {
        state.name: state
        for state in union.fta_states
    }

    assert states["q"].is_Initial is True
    assert states["2_q"].is_Initial is True


# ======================================================
# Test 15
# Invalid first FTA
# ======================================================

def test_union_rejects_invalid_first_fta():

    a = Ranked_Symbol(name="a", rank=0)
    q = State(name="q", is_Final=True)

    fta2 = make_fta(
        "fta2",
        [q],
        [a],
        [make_rule(a, [], q)]
    )

    with pytest.raises(icontract.ViolationError):
        RU(None, fta2).compute()


# ======================================================
# Test 16
# Invalid second FTA
# ======================================================

def test_union_rejects_invalid_second_fta():

    a = Ranked_Symbol(name="a", rank=0)
    q = State(name="q", is_Final=True)

    fta1 = make_fta(
        "fta1",
        [q],
        [a],
        [make_rule(a, [], q)]
    )

    with pytest.raises(icontract.ViolationError):
        RU(fta1, None).compute()