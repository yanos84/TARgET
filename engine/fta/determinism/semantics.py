from abc import ABC, abstractmethod

class AutomatonSemantics(ABC):
    '''
    Docstring for AutomatonSemantics
    This abstract class defines the semantics for different types of tree automata.
    Subclasses must implement the `transition_signature` method, which returns the key
    used for determinism checking for a given rule.
    '''
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
if __name__ == "__main__":
    from engine.fta.determinism.determinism import Determinism
    from fta.rankedfta import ranked_Fta
    from fta.rankedRule import ranked_Rule
    from fta.state import State
    from core.symbol import Ranked_Symbol

    # Define states
    s1 = State(name="q1", final=False, init=False)
    s2 = State(name="q2", final=False, init=False)
    s3 = State(name="q3", final=False, init=False)

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