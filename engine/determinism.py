
from fta.rankedfta import ranked_Fta
from fta.rankedRule import ranked_Rule
from fta.state import State
from core.symbol import Ranked_Symbol


def is_deterministic(fta: ranked_Fta) -> bool:
    """
    Checks whether the ranked finite tree automaton is deterministic
    (bottom-up determinism).

    Returns:
        bool: True if deterministic, False otherwise
    """

    # Dictionary:
    # key   = (symbol_name, tuple(input_state_names))
    # value = output_state_name
    transition_map = {}

    for rule in fta.transitions:

        # Optional: ensure rule validity
        if not rule.is_valid():
            return False

        symbol_key = rule.func.name
        input_key = tuple(state.name for state in rule.input)
        output_value = rule.output.name

        key = (symbol_key, input_key)

        if key in transition_map:
            # Same (symbol, inputs) but different output → nondeterministic
            if transition_map[key] != output_value:
                return False
        else:
            transition_map[key] = output_value

    return True



# Example usage

if __name__ == "__main__":

    # Define states
    s1 = State(name="q1", final=False, init=False)
    s2 = State(name="q2", final=False, init=False)
    s3 = State(name="q3", final=False, init=False)

    # Define ranked symbols
    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)

    # Define transition rules
    rule1 = ranked_Rule(symbol=f)
    rule1.input = [s1, s2]
    rule1.output = s3

    rule2 = ranked_Rule(symbol=f)
    rule2.input = [s1, s2]
    rule2.output = s3  # Same output as rule1 (deterministic)

    rule3 = ranked_Rule(symbol=f)
    rule3.input = [s2, s1]
    rule3.output = s3  # Different input order (still deterministic)

    # Create automaton
    automaton = ranked_Fta(
        fta_name="example_fta",
        alphabet=[f, a],
        fta_states=[s1, s2, s3],
        transitions=[rule1, rule2, rule3]
    )

    # Check determinism
    print("Is the automaton deterministic?", is_deterministic(automaton))