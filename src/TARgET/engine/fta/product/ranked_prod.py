from .abs_prod import Abs_prod
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.core.fta.rankedRule import ranked_Rule


class Ranked_prod(Abs_prod):
    """Class to compute the product of two ranked finite tree automata (RFTAs).
    The product of two RFTAs, RFTA1 and RFTA2, is a new RFTA that accepts exactly the trees that are accepted by both RFTA1 and RFTA2. This is achieved by constructing a new RFTA that combines the states and transitions of both RFT
    As while ensuring that the acceptance conditions reflect the intersection of the languages accepted by the original RFTAs. The resulting product RFTA can be used to check for common accepted trees between RFTA1 and RFTA2, or to perform operations like intersection and union with other RFTAs.
    Attributes:
    - None
    Methods:
    - __init__: Initializes the Ranked_prod class.
    - product: Computes the product of two ranked finite tree automata (RFTAs) and returns a new RFTA representing the product.
    """
    def __init__(self):
        super().__init__()

    def product(self, fta1: ranked_Fta, fta2: ranked_Fta) -> ranked_Fta:
        """
        Compute the product of two ranked finite tree automata.

        :param fta1: The first ranked finite tree automaton.
        :param fta2: The second ranked finite tree automaton.

        :returns: The product ranked finite tree automaton.
        """
        # Placeholder implementation
        # Actual product construction logic should be implemented here
        #red="\033[91m"
        #endc="\033[0m"
        prod_states = []
        prod_transitions = []
        for rule_A in fta1.transitions:
            for rule_B in fta2.transitions:
                if rule_A.func == rule_B.func:
                    input_states = []
                    for s1, s2 in zip(rule_A.input_states, rule_B.input_states):
                        input_states.append(
    State(
        name=f"({s1.name},{s2.name})",
        is_Final=s1.is_Final and s2.is_Final
    )
)
                    output_state = State(
    name=f"({rule_A.output_state.name},{rule_B.output_state.name})",
    is_Final=(
        rule_A.output_state.is_Final
        and rule_B.output_state.is_Final
    )
)
                    prod_rule = ranked_Rule(func=rule_A.func, input_states=input_states, output_state=output_state)
                    prod_states=list(set(prod_states + input_states + [output_state]))
                    prod_transitions.append(prod_rule)
        
        return ranked_Fta(fta_name=f"{fta1.name}_x_{fta2.name}", alphabet=fta1.alphabet, fta_states=prod_states, transitions=prod_transitions)

# Example usage

def make_rule(symbol, inputs, output):
    rule = ranked_Rule(func=symbol)
    rule.input_states = inputs
    rule.output_state = output
    return rule

if __name__ == "__main__": 
    from TARgET.core.fta.rankedfta import ranked_Fta, Ranked_Symbol, ranked_Rule, State
    from ..emptiness.ranked_emptiness import RankedEmptiness
    '''
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
    '''

    #____second example____(two automata with different symbols, the resulting product automaton should be empty)
    # ---------- FTA 1 ----------
    q1 = State(name="q1", is_Final=False)
    qf1 = State(name="qf1", is_Final=True)

    a = Ranked_Symbol(name="a", rank=0)
    f1 = Ranked_Symbol(name="f", rank=1)

    r1 = make_rule(a, [], q1)
    r2 = make_rule(f1, [q1], qf1)

    fta1 = ranked_Fta(
        fta_name="different_symbols_1",
        alphabet=[a, f1],
        fta_states=[q1, qf1],
        transitions=[r1, r2]
    )

    # ---------- FTA 2 ----------
    p1 = State(name="p1", is_Final=False)
    pf2 = State(name="pf2", is_Final=True)

    b = Ranked_Symbol(name="b", rank=0)
    f2 = Ranked_Symbol(name="f", rank=1)

    r3 = make_rule(b, [], p1)
    r4 = make_rule(f2, [p1], pf2)

    fta2 = ranked_Fta(
        fta_name="different_symbols_2",
        alphabet=[b, f2],
        fta_states=[p1, pf2],
        transitions=[r3, r4]
    )

    product_computer = Ranked_prod()
    product_automaton = product_computer.product(fta1, fta2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)
    #_____ testing if the automaton is empty or not____
    emptiness_checker = RankedEmptiness()
    is_empty = emptiness_checker.is_empty(product_automaton)
    if is_empty:
        print("The product automaton is empty")
    else:
        print("The product automaton is not empty")

    #___example 3_____
# ---------- FTA 1 ----------

    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)

    a1 = Ranked_Symbol(name="a", rank=0)

    r1 = make_rule(a1, [], q1)
    r2 = make_rule(a1, [], q2)

    fta1 = ranked_Fta(
        fta_name="multiple_nullary_1",
        alphabet=[a1],
        fta_states=[q1, q2],
        transitions=[r1, r2]
    )

    # ---------- FTA 2 ----------
    p1 = State(name="p1", is_Final=False)
    p2 = State(name="p2", is_Final=False)

    a2 = Ranked_Symbol(name="a", rank=0)

    r3 = make_rule(a2, [], p1)
    r4 = make_rule(a2, [], p2)

    fta2 = ranked_Fta(
        fta_name="multiple_nullary_2",
        alphabet=[a2],
        fta_states=[p1, p2],
        transitions=[r3, r4]
    )
    product_computer = Ranked_prod()
    product_automaton = product_computer.product(fta1, fta2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)

    '''
        the expected result :
        Fta name: multiple_nullary_1_x_multiple_nullary_2
        States list: (q1,p2) (is final :False),  (q2,p2) (is final :False),  (q1,p1) (is final :False),  (q2,p1) (is final :False),
        Alphabet: a(rank = 0),
        Rules list:
        a()---->(q1,p1)
        a()---->(q1,p2)
        a()---->(q2,p1)
        a()---->(q2,p2)
    '''
    #______Example 4______Binary symbol with multiple child combinations

    # ---------- FTA 1 ----------
    q1 = State(name="q1", is_Final=False)
    q2 = State(name="q2", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a1 = Ranked_Symbol(name="a", rank=0)
    f1 = Ranked_Symbol(name="f", rank=2)

    r1 = make_rule(a1, [], q1)
    r2 = make_rule(a1, [], q2)

    r3 = make_rule(f1, [q1, q2], qf)
    r4 = make_rule(f1, [q2, q1], qf)

    fta1 = ranked_Fta(
        fta_name="binary_1",
        alphabet=[a1, f1],
        fta_states=[q1, q2, qf],
        transitions=[r1, r2, r3, r4]
    )

    # ---------- FTA 2 ----------
    p1 = State(name="p1", is_Final=False)
    p2 = State(name="p2", is_Final=False)
    pf = State(name="pf", is_Final=True)

    a2 = Ranked_Symbol(name="a", rank=0)
    f2 = Ranked_Symbol(name="f", rank=2)

    r5 = make_rule(a2, [], p1)
    r6 = make_rule(a2, [], p2)

    r7 = make_rule(f2, [p1, p2], pf)
    r8 = make_rule(f2, [p2, p1], pf)

    fta2 = ranked_Fta(
        fta_name="binary_2",
        alphabet=[a2, f2],
        fta_states=[p1, p2, pf],
        transitions=[r5, r6, r7, r8]
    )

    product_computer = Ranked_prod()
    product_automaton = product_computer.product(fta1, fta2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)

# ______example 5 _____Same symbol name but different rank

    # ---------- FTA 1 ----------
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    a1 = Ranked_Symbol(name="a", rank=0)
    f_rank1 = Ranked_Symbol(name="f", rank=1)

    r1 = make_rule(a1, [], q1)
    r2 = make_rule(f_rank1, [q1], qf)

    fta1 = ranked_Fta(
        fta_name="different_rank_1",
        alphabet=[a1, f_rank1],
        fta_states=[q1, qf],
        transitions=[r1, r2]
    )

    # ---------- FTA 2 ----------
    p1 = State(name="p1", is_Final=False)
    pf = State(name="pf", is_Final=True)

    a2 = Ranked_Symbol(name="a", rank=0)
    f_rank2 = Ranked_Symbol(name="f", rank=2)

    r3 = make_rule(a2, [], p1)
    r4 = make_rule(f_rank2, [p1, p1], pf)

    fta2 = ranked_Fta(
        fta_name="different_rank_2",
        alphabet=[a2, f_rank2],
        fta_states=[p1, pf],
        transitions=[r3, r4]
    )

    product_computer = Ranked_prod()
    product_automaton = product_computer.product(fta1, fta2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)

#______example 6 _____ Final-state mismatch

    qf = State(name="qf", is_Final=True)
    p1 = State(name="p1", is_Final=False)

    a1 = Ranked_Symbol(name="a", rank=0)
    a2 = Ranked_Symbol(name="a", rank=0)

    r1 = make_rule(a1, [], qf)
    r2 = make_rule(a2, [], p1)

    fta1 = ranked_Fta(
        fta_name="final_mismatch_1",
        alphabet=[a1],
        fta_states=[qf],
        transitions=[r1]
    )

    fta2 = ranked_Fta(
        fta_name="final_mismatch_2",
        alphabet=[a2],
        fta_states=[p1],
        transitions=[r2]
    )
    product_computer = Ranked_prod()
    product_automaton = product_computer.product(fta1, fta2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)

#_____example 7 _____ Same product state generated multiple times, This specifically tests State.__eq__ and State.__hash__.
    q = State(name="q", is_Final=False)

    a1 = Ranked_Symbol(name="a", rank=0)
    b1 = Ranked_Symbol(name="b", rank=0)

    r1 = make_rule(a1, [], q)
    r2 = make_rule(b1, [], q)

    fta1 = ranked_Fta(
        fta_name="duplicate_states_1",
        alphabet=[a1, b1],
        fta_states=[q],
        transitions=[r1, r2]
    )

    p = State(name="p", is_Final=False)

    a2 = Ranked_Symbol(name="a", rank=0)
    b2 = Ranked_Symbol(name="b", rank=0)

    r3 = make_rule(a2, [], p)
    r4 = make_rule(b2, [], p)

    fta2 = ranked_Fta(
        fta_name="duplicate_states_2",
        alphabet=[a2, b2],
        fta_states=[p],
        transitions=[r3, r4]
    )
    product_computer = Ranked_prod()
    product_automaton = product_computer.product(fta1, fta2)
    print(f"Product automaton name: {product_automaton.name}")
    print(f"Number of states in product automaton: {len(product_automaton.fta_states)}")
    print(f"Number of transitions in product automaton: {len(product_automaton.transitions)}")  
    print(product_automaton)