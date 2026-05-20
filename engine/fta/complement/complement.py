from fta.abst_fta import Fta
from fta.state import State
from typing import List
from core.symbol import Symbol, Ranked_Symbol
import copy

class Complement():
    """Class to compute the complement of a finite tree automaton (FTA).
    The complement of an FTA is a new FTA that accepts exactly the trees that the original FTA does not accept. This is achieved by negating the acceptance conditions of the states and transitions in the original FTA. The resulting complement FTA can be used to check for non-acceptance of trees or to perform operations like intersection and union with other FTAs.
    Attributes:
    - fta: The original finite tree automaton for which the complement is to be computed.
    Methods:
    - __init__: Initializes the Complement class with a given FTA. """

    def __init__(self, fta: Fta) -> None:
        self.fta = copy.deepcopy(fta)
    
    def compute_complement(self) -> Fta:
        # Placeholder for complement computation logic
        # This should return a new Fta instance representing the complement of self.fta
        alphabet =getattr(self.fta, 'alphabet', None)
        if alphabet is not None and isinstance(alphabet, list):
            for sym in alphabet:
                if not isinstance(sym, Symbol):
                    raise TypeError("Alphabet must contain only Symbol instances.")
            for state in self.fta.fta_states:
                state.is_Final = not state.is_Final
            for r in self.fta.transitions:
                for input in r.input_states:
                    input.is_Final = not input.is_Final
                r.output_state.is_Final = not r.output_state.is_Final
            return self.fta
        else:
            raise TypeError("Alphabet must be a list of Symbol instances.")


## Example usage
if __name__ == "__main__":
    from fta.rankedfta import ranked_Fta
    s1 = State(name="q0", is_Final=True)
    s2 = State(name="q1", is_Final=False)
    states = [s1, s2]
    fta = ranked_Fta(fta_name="example_fta", fta_states=states, alphabet=[Ranked_Symbol(name="a", rank=0)], transitions=[])

    complement_calculator = Complement(fta)
    complement_fta = complement_calculator.compute_complement()  
    print("Original FTA:",fta) 
    print("Complement FTA:",complement_fta)