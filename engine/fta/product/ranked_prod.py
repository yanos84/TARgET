from .abs_prod import Abs_prod
from fta.rankedfta import ranked_Fta
from fta.state import State
from fta.rankedRule import ranked_Rule


class Ranked_prod(Abs_prod):
    def __init__(self):
        super().__init__()

    def product(self, fta1: ranked_Fta, fta2: ranked_Fta) -> ranked_Fta:
        """Compute the product of two ranked finite tree automata.
        Args:
            fta1 (ranked_Fta): The first ranked finite tree automaton.
            fta2 (ranked_Fta): The second ranked finite tree automaton.
        Returns:
            ranked_Fta: The product ranked finite tree automaton.
        """
        # Placeholder implementation
        # Actual product construction logic should be implemented here
        red="\033[91m"
        endc="\033[0m"
        prod_states = []
        prod_transitions = []
        for rule_A in fta1.transitions:
            for rule_B in fta2.transitions:
                if rule_A.func == rule_B.func:
                    input_states = []
                    for s1, s2 in zip(rule_A.input_states, rule_B.input_states):
                        input_states.append(State(name=f"{red}{"("}{s1.name},{s2.name}{")"}{endc}", is_Final=s1.is_Final and s2.is_Final))
                    output_state = State(name=f"{red}{"("}{rule_A.output_state.name},{rule_B.output_state.name}{")"}{endc}", is_Final=rule_A.output_state.is_Final and rule_B.output_state.is_Final)
                    prod_rule = ranked_Rule(func=rule_A.func, input_states=input_states, output_state=output_state)
                    prod_states=list(set(prod_states + input_states + [output_state]))
                    prod_transitions.append(prod_rule)
        
        return ranked_Fta(fta_name=f"{fta1.name}_x_{fta2.name}", alphabet=fta1.alphabet, fta_states=prod_states, transitions=prod_transitions)

# Example usage
if __name__ == "__main__": 
    from fta.rankedfta import ranked_Fta, Ranked_Symbol, ranked_Rule, State

    s1 = State(name="q1", is_Final=False)
    t1 = State(name="q2", is_Final=True)
    st1 = [s1, t1]
    symb1 = Ranked_Symbol(name="f", rank=2)
    rule1 = ranked_Rule(func=symb1)
    rule1.input_states = [s1, s1]
    rule1.output_state = t1
    rules1 = [rule1]
    alpha1 = [symb1]
    automaton1 = ranked_Fta(fta_name="fta1", alphabet=alpha1, fta_states=st1, transitions=rules1)

    s2 = State(name="p1", is_Final=False)
    t2 = State(name="p2", is_Final=True)
    st2 = [s2, t2]
    symb2 = Ranked_Symbol(name="f", rank=2)
    rule2 = ranked_Rule(func=symb2)
    rule2.input_states = [s2, s2]
    rule2.output_state = t2
    rules2 = [rule2]
    alpha2 = [symb2]
    automaton2 = ranked_Fta(fta_name="fta2", alphabet=alpha2, fta_states=st2, transitions=rules2)

    product_computer = Ranked_prod()
    product_automaton = product_computer.product(automaton1, automaton2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)