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

if __name__ == "__main__":
    from TARgET.core.algebraic.stochastic_semiring import ProbabilitySemiring
    from TARgET.core.algebraic.bool_semiring import BooleanSemiring
    from TARgET.core.base.symbol import Ranked_Symbol
    from TARgET.core.fta.rankedRule import ranked_Rule
    from TARgET.core.base.rankedTree import RankedTree
    from .rankedAcceptor import RankedBottomUpAcceptor

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