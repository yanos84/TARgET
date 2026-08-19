from .abs_diff import Abs_Diff
from TARgET.core.fta.rankedfta import ranked_Fta
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
        Compute the difference between two ranked finite tree automata.

        The resulting automaton recognizes:

            L(fta1) - L(fta2)

        Both automata are considered over the union of their alphabets before
        complement, determinization, and product are performed.
        """

        # --------------------------------------------------
        # Step 1: Construct the common alphabet
        # --------------------------------------------------

        common_alphabet = list(fta1.alphabet)

        for symbol in fta2.alphabet:
            if symbol not in common_alphabet:
                common_alphabet.append(symbol)

        # --------------------------------------------------
        # Step 2: Rebuild both FTAs over the common alphabet
        # --------------------------------------------------

        fta1_common = ranked_Fta(
            fta_name=f"{fta1.name}_common",
            alphabet=common_alphabet,
            fta_states=fta1.fta_states,
            transitions=fta1.transitions,
        )

        fta2_common = ranked_Fta(
            fta_name=f"{fta2.name}_common",
            alphabet=common_alphabet,
            fta_states=fta2.fta_states,
            transitions=fta2.transitions,
        )

        # --------------------------------------------------
        # Step 3: Complement the second FTA
        # --------------------------------------------------

        complement_calculator = Complement(fta2_common)
        fta2_complement = complement_calculator.compute_complement()

        # --------------------------------------------------
        # Step 4: Determinize both automata
        # --------------------------------------------------

        det_fta1 = det.determinize(fta1_common)
        det_fta2_complement = det.determinize(fta2_complement)

        # --------------------------------------------------
        # Step 5: Product
        # --------------------------------------------------

        product_computer = Ranked_prod()

        return product_computer.product(
            det_fta1,
            det_fta2_complement,
        )

    def is_equivalent(self, fta1: ranked_Fta, fta2: ranked_Fta) -> bool:
        """
        Check whether two ranked finite tree automata (RFTAs) are equivalent.

        Two RFTAs are equivalent if neither language contains a tree that is
        absent from the other language. This is checked by computing both
        differences and verifying that both resulting languages are empty.

        :param fta1: The first ranked finite tree automaton.
        :param fta2: The second ranked finite tree automaton.

        :returns: ``True`` if the automata are equivalent; otherwise, ``False``.
        :rtype: bool
        """
        emptiness_checker = RankedEmptiness()

        difference_1 = self.diff(fta1, fta2)
        difference_2 = self.diff(fta2, fta1)

        return (
            emptiness_checker.is_empty(difference_1)
            and emptiness_checker.is_empty(difference_2)
        )


# Example usage
if __name__ == "__main__":
    from TARgET.core.fta.rankedfta import ranked_Fta, Ranked_Symbol, ranked_Rule, State

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