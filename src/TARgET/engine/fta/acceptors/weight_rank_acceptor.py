from typing import Dict
from .acceptor import Acceptor
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.base.rankedTree import RankedTree
from TARgET.core.fta.state import State
from TARgET.core.algebraic.semiring import Semiring


class WeightedRankedBottomUpAcceptor(Acceptor):
    """
    Bottom-up acceptor for Weighted Ranked Finite Tree Automata (WRFTA).

    Computes, for a given tree, the weight associated with each possible
    root state using the automaton's semiring.
    """

    def compute_weights(
        self,
        automaton: ranked_Fta,
        tree: RankedTree
    ) -> Dict[State, Semiring]:
        """
        Compute the weights for each possible root state of the given tree.
        Returns a dictionary mapping each state to its corresponding weight.
        """

        # 1️⃣ Base: compute weights for children
        children_weights = [
            self.compute_weights(automaton, child)
            for child in tree.children
        ]

        result: Dict[State, Semiring] = {}

        # 2️⃣ Apply weighted rules
        for rule in automaton.transitions:

            if rule.func != tree.ranked_symbol:
                continue

            if len(rule.input_states) != len(children_weights):
                continue

            # ⊗ combine children weights
            #weight = rule.weight.semiring.one()
            Semiring_ = automaton.get_semiring()
            weight = Semiring_.one()
            #from algebric.stochastic_semiring import ProbabilitySemiring
            #weight = ProbabilitySemiring.one()

            compatible = True
            for expected_state, child_map in zip(rule.input_states, children_weights):
                if expected_state not in child_map:
                    compatible = False
                    break
                weight = weight * child_map[expected_state]

            if not compatible:
                continue

            # include rule weight
            weight = weight * rule.weight

            # ⊕ aggregate into output state
            q = rule.output_state
            if q in result:
                result[q] = result[q] + weight
            else:
                result[q] = weight

        return result

    def accepts(
        self,
        automaton: ranked_Fta,
        tree: RankedTree
    ) -> Semiring:
        """
        Returns the total acceptance weight of the tree.
        """

        root_weights = self.compute_weights(automaton, tree)
        _Semiring = automaton.get_semiring()
        total = _Semiring.zero()
        #from algebric.stochastic_semiring import ProbabilitySemiring
        #total = ProbabilitySemiring.zero()
        for state, weight in root_weights.items():
            if state.is_Final:
                total = total + weight

        return total

#Example_usage

#______Example1_____ general example of a weighted ranked bottom up acceptor

def general_example():
    s= State(name="q1", is_Final=False)
    t=State(name="q2", is_Final=False)
    u=State(name="q3", is_Final=True)
    st = []
    st.append(s)
    st.append(t)
    f = Ranked_Symbol(name="f", rank=2)
    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    rule = ranked_Rule(func = f, is_weighted = True, weight = ProbabilitySemiring(0.3))
    rule.input_states = st
    rule.output_state = u
    rules = []
    rules.append(rule)
    #rules.append(rule)
    rules.append(ranked_Rule(a, [], s, is_weighted=True, weight=ProbabilitySemiring(0.1)))
    rules.append(ranked_Rule(b, [], t, is_weighted=True, weight=ProbabilitySemiring(0.2)))
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

    print(root)  # Output: f(a,b)
    acceptor = RankedBottomUpAcceptor()

    if acceptor.accepts(automaton, root):
        print("Tree accepted")
    else:
        print("Tree rejected")
    
    weight_acceptor = WeightedRankedBottomUpAcceptor()
    print(weight_acceptor.accepts(automaton=automaton, tree=root))

# ______example 2______ weighted nullary example

def weighted_nullary_example():
    """
    Test:

        a() -> qf [0.5]

    qf is final.

    Expected acceptance weight: 0.5
    """


    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    qf = State(name="qf", is_Final=True)

    rule = ranked_Rule(
        func=a,
        input_states=[],
        output_state=qf,
        is_weighted=True,
        weight=ProbabilitySemiring(0.5),
    )

    automaton = ranked_Fta(
        fta_name="weighted_nullary",
        alphabet=[a],
        fta_states=[qf],
        transitions=[rule],
    )

    acceptor = WeightedRankedBottomUpAcceptor()

    result = acceptor.accepts(automaton, tree)

    print("Acceptance weight:", result)

# ______example 3______ 

def weighted_binary_example():
    """
    Test:

        a()      -> q0 [0.2]
        b()      -> q1 [0.3]
        f(q0,q1) -> qf [0.5]

    Expected acceptance weight:

        0.2 * 0.3 * 0.5 = 0.03
    """

    a = Ranked_Symbol(name="a", rank=0)
    b = Ranked_Symbol(name="b", rank=0)
    f = Ranked_Symbol(name="f", rank=2)

    tree = RankedTree(symbol=f)
    tree.add_child(RankedTree(symbol=a))
    tree.add_child(RankedTree(symbol=b))

    q0 = State(name="q0", is_Final=False)
    q1 = State(name="q1", is_Final=False)
    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(
            a, [], q0,
            is_weighted=True,
            weight=ProbabilitySemiring(0.2),
        ),
        ranked_Rule(
            b, [], q1,
            is_weighted=True,
            weight=ProbabilitySemiring(0.3),
        ),
        ranked_Rule(
            f, [q0, q1], qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.5),
        ),
    ]

    automaton = ranked_Fta(
        fta_name="weighted_binary",
        alphabet=[a, b, f],
        fta_states=[q0, q1, qf],
        transitions=rules,
    )

    acceptor = WeightedRankedBottomUpAcceptor()

    result = acceptor.accepts(automaton, tree)

    print("Acceptance weight:", result)

# ______example 4______ weighted multiple rules example

def weighted_multiple_rules_example():
    """
    Two rules produce the same final state:

        a() -> qf [0.2]
        a() -> qf [0.3]

    Expected acceptance weight: 0.5
    """

    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    qf = State(name="qf", is_Final=True)

    rules = [
        ranked_Rule(
            a, [], qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.2),
        ),
        ranked_Rule(
            a, [], qf,
            is_weighted=True,
            weight=ProbabilitySemiring(0.3),
        ),
    ]

    automaton = ranked_Fta(
        fta_name="weighted_multiple_rules",
        alphabet=[a],
        fta_states=[qf],
        transitions=rules,
    )

    acceptor = WeightedRankedBottomUpAcceptor()

    result = acceptor.accepts(automaton, tree)

    print("Acceptance weight:", result)

#_____Example 5______ Weighted multiple final states example

def weighted_multiple_final_states_example():
    """
    Two final states are reachable:

        a() -> q1 [0.2]
        a() -> q2 [0.3]

    Expected acceptance weight: 0.5
    """

    a = Ranked_Symbol(name="a", rank=0)

    tree = RankedTree(symbol=a)

    q1 = State(name="q1", is_Final=True)
    q2 = State(name="q2", is_Final=True)

    rules = [
        ranked_Rule(
            a, [], q1,
            is_weighted=True,
            weight=ProbabilitySemiring(0.2),
        ),
        ranked_Rule(
            a, [], q2,
            is_weighted=True,
            weight=ProbabilitySemiring(0.3),
        ),
    ]

    automaton = ranked_Fta(
        fta_name="weighted_multiple_final",
        alphabet=[a],
        fta_states=[q1, q2],
        transitions=rules,
    )

    acceptor = WeightedRankedBottomUpAcceptor()

    result = acceptor.accepts(automaton, tree)

    print("Acceptance weight:", result)

if __name__ == "__main__":
    from TARgET.core.algebraic.stochastic_semiring import ProbabilitySemiring
    from TARgET.core.algebraic.bool_semiring import BooleanSemiring
    from TARgET.core.base.symbol import Ranked_Symbol
    from TARgET.core.fta.rankedRule import ranked_Rule
    from TARgET.core.base.rankedTree import RankedTree
    from .rankedAcceptor import RankedBottomUpAcceptor

    general_example()

    weighted_nullary_example()  # Expected weight: 0.5
    weighted_binary_example()   # Expected weight: 0.03
    weighted_multiple_rules_example()  # Expected weight: 0.5
    weighted_multiple_final_states_example()  # Expected weight: 0.5