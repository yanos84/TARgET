from fta.abst_fta import Fta
from fta.state import State
from typing import List
from core.symbol import Symbol, Ranked_Symbol
import copy

class Complement():

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
            for state in self.fta.states_list:
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
    s1 = State(name="q0", final=True)
    s2 = State(name="q1", final=False)
    states = [s1, s2]
    fta = ranked_Fta(fta_name="example_fta", fta_states=states, alphabet=[Ranked_Symbol(name="a", rank=0)], transitions=[])

    complement_calculator = Complement(fta)
    complement_fta = complement_calculator.compute_complement()  
    print("Original FTA:",fta) 
    print("Complement FTA:",complement_fta)