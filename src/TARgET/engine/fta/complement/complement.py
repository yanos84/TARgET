from TARgET.core.fta.abst_fta import Fta
from TARgET.core.fta.state import State
#from typing import List
from TARgET.core.base.symbol import Symbol, Ranked_Symbol
from ..determinism.determinism import Determinism
from ..determinism.semantics import BottomUpRankedSemantics
from ..determinization.ranked_determinization import determinize
from ..completion.ranked_completion import Completion
import copy

class Complement():
    """Class to compute the complement of a finite tree automaton (FTA).
    The complement of an FTA is a new FTA that accepts exactly the trees that the original FTA does not accept. This is achieved by negating the acceptance conditions of the states and transitions in the original FTA. The resulting complement FTA can be used to check for non-acceptance of trees or to perform operations like intersection and union with other FTAs.
    Attributes:
        - fta: The finite tree automaton (FTA) for which the complement is to be computed.
    Methods:
        - __init__: Initializes the Complement class with a given FTA. """

    def __init__(self, fta: Fta) -> None:
        self.fta = copy.deepcopy(fta)
    
    def compute_complement(self) -> Fta:
        semantics = BottomUpRankedSemantics()

        if not Determinism.check(self.fta.transitions, semantics):
            self.fta = determinize(self.fta)

        self.fta = Completion(
            fta=self.fta
        ).compute_completion()

        alphabet = getattr(self.fta, "alphabet", None)

        if alphabet is None or not isinstance(alphabet, list):
            raise TypeError(
                "Alphabet must be a list of Symbol instances."
            )

        for sym in alphabet:
            if not isinstance(sym, Symbol):
                raise TypeError(
                    "Alphabet must contain only Symbol instances."
                )

        # Complement: flip final states exactly once.
        for state in self.fta.fta_states:
            state.is_Final = not state.is_Final

        return self.fta

## Example usage

#_____example 0____ general one 

def ground_example_complement():
    s1 = State(name="q0", is_Final=True)
    s2 = State(name="q1", is_Final=False)
    states = [s1, s2]
    fta = ranked_Fta(fta_name="example_fta", fta_states=states, alphabet=[Ranked_Symbol(name="a", rank=0)], transitions=[])

    complement_calculator = Complement(fta)
    complement_fta = complement_calculator.compute_complement()  
    print("Original FTA:",fta) 
    print("Complement FTA:",complement_fta)

#_____Example 1______ Complement of an FTA with no final states

def test_complement_empty_fta():
    """Complement of an FTA with no final states."""

    q0 = State(name="q0", is_Final=False)

    a = Ranked_Symbol(name="a", rank=0)

    fta = ranked_Fta(
        fta_name="empty_fta",
        fta_states=[q0],
        alphabet=[a],
        transitions=[],
    )

    complement = Complement(fta).compute_complement()

    print("Original FTA:",fta) 
    print("Complement FTA:",complement)

    assert complement is not fta
    assert complement.fta_states[0].is_Final is True

    # Original must remain unchanged
    assert q0.is_Final is False

#_____Example 2______ 
def test_complement_empty_language():
    """Complement of an FTA with an empty language."""

    q0 = State("q0", is_Final=False)

    a = Ranked_Symbol("a", rank=0)

    fta = ranked_Fta(
        fta_name="empty_language",
        alphabet=[a],
        fta_states=[q0],
        transitions=[]
    )

    complement = Complement(fta)
    comp_fta = complement.compute_complement()

    print("\nOriginal FTA:")
    print(fta)

    print("\nComplement FTA:")
    print(comp_fta)

def test_complement_completes_fta():
    q0 = State("q0", is_Final=True)

    a = Ranked_Symbol("a", rank=0)
    f = Ranked_Symbol("f", rank=1)

    fta = ranked_Fta(
        alphabet=[a, f],
        fta_states=[q0],
        transitions=[]
    )

    comp_fta = Complement(fta).compute_complement()

    print("States:", [s.name for s in comp_fta.fta_states])
    print("Transitions:", comp_fta.transitions)

    assert [s.name for s in fta.fta_states] == ["q0"]

if __name__ == "__main__":
    from TARgET.core.fta.rankedfta import ranked_Fta

    #ground_example_complement()
    #test_complement_empty_fta()
    #test_complement_empty_language()
    test_complement_completes_fta()