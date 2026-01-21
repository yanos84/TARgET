from .abs_diff import Abs_Diff
from fta.rankedfta import ranked_Fta
from engine.fta.complement.complement import Complement
import engine.fta.determinization.ranked_determinization as det
from engine.fta.product.ranked_prod import Ranked_prod
from engine.fta.emptiness.ranked_emptiness import RankedEmptiness

class Ranked_Diff(Abs_Diff):
    def __init__(self):
        super().__init__()
    
    def diff(self, fta1: ranked_Fta, fta2: ranked_Fta) -> ranked_Fta:
        # Step 1: Compute the complement of fta2
        complement_calculator = Complement(fta2)
        fta2_complement = complement_calculator.compute_complement()
        
        # Step 2: Determinize both fta1 and the complement of fta2
        det_fta1 = det.determinize(fta1)
        det_fta2_complement = det.determinize(fta2_complement)
        product_computer = Ranked_prod()
        product_automaton = product_computer.product(det_fta1, det_fta2_complement)
     
        return product_automaton

    def is_equivalent(self, fta1: ranked_Fta, fta2: ranked_Fta) -> bool:
        difference_fta = self.diff(fta1, fta2)
        emptiness_checker = RankedEmptiness()
        return emptiness_checker.is_empty(difference_fta)


# Example usage
if __name__ == "__main__":
    from fta.rankedfta import ranked_Fta, Ranked_Symbol, ranked_Rule, State

    # Define fta1
    s1 = State(name="q1", is_Final=True)
    t1 = State(name="q2", is_Final=False)
    st1 = [s1, t1]
    symb1 = Ranked_Symbol(name="f", rank=2)
    rule1 = ranked_Rule(func=symb1)
    rule1.input_states = [s1, s1]
    rule1.output_state = t1
    rules1 = [rule1]
    alpha1 = [symb1]
    automaton1 = ranked_Fta(fta_name="fta1", alphabet=alpha1, fta_states=st1, transitions=rules1)

    # Define fta2
    s2 = State(name="p1", is_Final=False)
    t2 = State(name="p2", is_Final=True)
    st2 = [s2, t2]
    symb2 = Ranked_Symbol(name="f", rank=2)
    rule2 = ranked_Rule(func=symb2)
    rule2.input_states= [s2, s2]
    rule2.output_state = t2
    rules2 = [rule2]
    alpha2 = [symb2]
    automaton2 = ranked_Fta(fta_name="fta2", alphabet=alpha2, fta_states=st2, transitions=rules2)

    # Compute the difference fta1 - fta2
    diff_calculator = Ranked_Diff()
    difference_automaton = diff_calculator.diff(automaton1, automaton2)
    print("FTA 1:", automaton1)
    print("FTA 2:", automaton2)
    print("Difference FTA (FTA 1 - FTA 2):", difference_automaton)
    print("Is FTA 1 equivalent to FTA 2?", diff_calculator.is_equivalent(automaton1, automaton2))