from abc import ABC, abstractmethod
from .determinism import Determinism

class AutomatonSemantics(ABC):
    """
    This abstract class defines the semantics for different types of tree automata.
    Subclasses must implement the `transition_signature` method, which returns the key
    used for determinism checking for a given rule.
    """
    @abstractmethod
    def transition_signature(self, rule):
        """
        Returns (key, output) used for determinism checking.
        """
        pass


class BottomUpRankedSemantics(AutomatonSemantics):

    def transition_signature(self, rule):


        # Optional structural validation
        if hasattr(rule, "is_valid") and not rule.is_valid():
            raise ValueError("Invalid ranked rule")

        symbol_key = rule.func.name
        input_key = tuple(state.name for state in rule.input_states)
        output_value = rule.output_state.name

        key = (symbol_key, input_key)
        return key, output_value

class TopDownRankedSemantics:
    def transition_signature(self, rule):
        key = (rule.input_state.name, rule.func.name)
        output = tuple(s.name for s in rule.output_states)
        return key, output
    

class HedgeSemantics:
    def transition_signature(self, rule):
        key = (rule.state.name, rule.symbol.name, rule.position)
        output = rule.regex
        return key, output




#example usage

#___example1____ general determinism check for ranked FTA using BottomUpRankedSemantics

def check_determinism_for_ranked_fta(ranked_fta):

    # Define states
    s1 = State(name="q1", is_Final=False)
    s2 = State(name="q2", is_Final=False)
    s3 = State(name="q3", is_Final=False)

    # Define ranked symbols
    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)

    # Define transition rules
    rule1 = ranked_Rule(func=f)
    rule1.input_states = [s1, s2]
    rule1.output_state = s3

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [s1, s2]
    rule2.output_state = s3  # Same output as rule1 (deterministic)

    rule3 = ranked_Rule(func=f)
    rule3.input_states = [s2, s1]
    rule3.output_state = s3  # Different input order (still deterministic)

    # Create automaton
    automaton = ranked_Fta(
        fta_name="example_fta",
        alphabet=[f, a],
        fta_states=[s1, s2, s3],
        transitions=[rule1, rule2, rule3]
    )


    # Check determinism using BottomUpRankedSemantics
    semantics = BottomUpRankedSemantics()
    is_deterministic = Determinism.check(automaton.transitions, semantics)
    print(f"The ranked FTA is deterministic: {is_deterministic}")

#______example2____ empty ranked FTA determinism check
def test_determinism_empty():
    semantics = BottomUpRankedSemantics()

    assert Determinism.check([], semantics) is True

#_____example3____ single transition determinism check

def test_determinism_single_transition():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule = ranked_Rule(func=f)
    rule.input_states = [q0]
    rule.output_state = q1

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule], semantics) is True

#_____example4____ duplicate transition determinism check   

def test_determinism_duplicate_rule():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = ranked_Rule(func=f)
    rule1.input_states = [q0]
    rule1.output_state = q1

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [q0]
    rule2.output_state = q1

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule1, rule2], semantics) is True

#_____example5____ nondeterminism check with same LHS but different output  

def test_nondeterminism_same_lhs_different_output():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = ranked_Rule(func=f)
    rule1.input_states = [q0]
    rule1.output_state = q1

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [q0]
    rule2.output_state = q2

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule1, rule2], semantics) is False

#_____example6____ determinism check with same symbol but different input states

def test_determinism_same_symbol_different_input():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rule1 = ranked_Rule(func=f)
    rule1.input_states = [q0]
    rule1.output_state = q2

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [q1]
    rule2.output_state = q2

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule1, rule2], semantics) is True


#_____example7____ determinism check with reversed input states for the same symbol 

def test_determinism_reversed_arguments():
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)

    f = Ranked_Symbol(name="f", rank=2)

    rule1 = ranked_Rule(func=f)
    rule1.input_states = [q1, q2]
    rule1.output_state = q3

    rule2 = ranked_Rule(func=f)
    rule2.input_states = [q2, q1]
    rule2.output_state = q3

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule1, rule2], semantics) is True

#_____example8____ determinism check for nullary symbol

def test_determinism_nullary():
    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rule = ranked_Rule(func=a)
    rule.input_states = []
    rule.output_state = q0

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule], semantics) is True

#_____example9____ determinism check for multiple identical nullary rules

def test_determinism_multiple_identical_nullary_rules():
    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rules = []

    for _ in range(100):
        rule = ranked_Rule(func=a)
        rule.input_states = []
        rule.output_state = q0
        rules.append(rule)

    semantics = BottomUpRankedSemantics()

    assert Determinism.check(rules, semantics) is True

#_____example10____ nondeterminism check for nullary symbol with different outputs

def test_nondeterminism_nullary_different_outputs():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    rule1 = ranked_Rule(func=a)
    rule1.input_states = []
    rule1.output_state = q0

    rule2 = ranked_Rule(func=a)
    rule2.input_states = []
    rule2.output_state = q1

    semantics = BottomUpRankedSemantics()

    assert Determinism.check([rule1, rule2], semantics) is False

#_____example11____ nondeterminism check for multiple outputs for the same input

def test_nondeterminism_multiple_outputs():
    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    q3 = State(name="q3", is_Final=False)

    f = Ranked_Symbol(name="f", rank=1)

    rules = []

    for output in [q1, q2, q3]:
        rule = ranked_Rule(func=f)
        rule.input_states = [q0]
        rule.output_state = output
        rules.append(rule)

    semantics = BottomUpRankedSemantics()

    assert Determinism.check(rules, semantics) is False

#_____example12____ determinism check for many rules

def test_determinism_many_rules():
    states = [
        State(name=f"q{i}", is_Final=False)
        for i in range(100)
    ]

    f = Ranked_Symbol(name="f", rank=1)

    rules = []

    for i in range(100):
        rule = ranked_Rule(func=f)
        rule.input_states = [states[i]]
        rule.output_state = states[(i + 1) % 100]
        rules.append(rule)

    semantics = BottomUpRankedSemantics()

    assert Determinism.check(rules, semantics) is True

if __name__ == "__main__":
    from .determinism import Determinism
    from TARgET.core.fta.rankedfta import ranked_Fta
    from TARgET.core.fta.rankedRule import ranked_Rule
    from TARgET.core.fta.state import State
    from TARgET.core.base.symbol import Ranked_Symbol
    check_determinism_for_ranked_fta(None)
    test_determinism_empty()
    test_determinism_single_transition()
    test_determinism_duplicate_rule()
    test_nondeterminism_same_lhs_different_output()
    test_determinism_same_symbol_different_input()
    test_determinism_reversed_arguments()
    test_determinism_nullary()
    test_determinism_multiple_identical_nullary_rules()
    test_nondeterminism_nullary_different_outputs()
    test_nondeterminism_multiple_outputs()
    test_determinism_many_rules()