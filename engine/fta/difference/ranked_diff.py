from .abs_diff import Abs_Diff
from TARgET.fta.rankedfta import ranked_Fta
from TARgET.engine.fta.complement.complement import Complement
import TARgET.engine.fta.determinization.ranked_determinization as det
from TARgET.engine.fta.product.ranked_prod import Ranked_prod
from TARgET.engine.fta.emptiness.ranked_emptiness import RankedEmptiness

class Ranked_Diff(Abs_Diff):
    """Class to compute the difference between two ranked finite tree automata (RFTAs).
    The difference of two RFTAs, RFTA1 and RFTA2, is a new RFTA that accepts exactly the trees that are accepted by RFTA1 but not by RFTA2. This is achieved by constructing a new RFTA that combines the states and transitions of both RFTAs while ensuring that the acceptance conditions reflect the difference. The resulting difference RFTA can be used
    to check for non-acceptance of trees in RFTA2 that are accepted by RFTA1, or to perform operations like intersection and union with other RFTAs.
    Attributes:
    - None
    Methods:
    - __init__: Initializes the Ranked_Diff class.
    - diff: Computes the difference between two ranked finite tree automata (RFTAs) and returns a new RFTA representing the difference.
    - is_equivalent: Checks if two RFTAs are equivalent by computing their difference and checking if the resulting difference RFTA is empty (i.e., accepts no trees).
    """
    def __init__(self):
        super().__init__()
    
    def diff(self, fta1: ranked_Fta, fta2: ranked_Fta) -> ranked_Fta:
        """
        Compute the difference between two ranked finite tree automata (RFTAs).
        Args:
            fta1: The first ranked finite tree automaton.
            fta2: The second ranked finite tree automaton.
        Returns:   
            ranked_Fta: A new ranked finite tree automaton that accepts exactly the trees accepted by fta1 but not by fta2.
        """
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
        """
        Check whether two ranked finite tree automata (RFTAs) are equivalent by computing the difference and checking for emptiness.
        Args:
            fta1: The first ranked finite tree automaton.
            fta2: The second ranked finite tree automaton.
        Returns:   
            bool: True if the RFTAs are equivalent, False otherwise.
        """
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