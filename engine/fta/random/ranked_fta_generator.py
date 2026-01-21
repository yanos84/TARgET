import random
from typing import List
from fta.rankedfta import ranked_Fta
from fta.state import State
from core.symbol import Ranked_Symbol
from fta.rankedRule import ranked_Rule
from .randomGenerator import FtaGenerator



class RandomRankedFtaGenerator(FtaGenerator):

    def __init__(
        self,
        fta_name: str = "random_fta",
        n_states: int = 5,
        n_symbols: int = 3,
        max_rank: int = 3,
        n_rules: int = 10,
        final_ratio: float = 0.3,
        seed: int | None = None
    ):
        self.fta_name = fta_name
        self.n_states = n_states
        self.n_symbols = n_symbols
        self.max_rank = max_rank
        self.n_rules = n_rules
        self.final_ratio = final_ratio
        if seed is not None:
            random.seed(seed)

    def generate(self) -> ranked_Fta:



        """
        Generates a random ranked finite tree automaton (FTA).

        Parameters:
        - fta_name: Name of the FTA.
        - n_states: Number of states in the FTA.
        - n_symbols: Number of ranked symbols in the alphabet.
        - max_rank: Maximum rank for the ranked symbols.
        - n_rules: Number of transition rules in the FTA.
        - final_ratio: Ratio of final states among all states.

        Returns:
        - An instance of ranked_Fta representing the random FTA.
        """

        # Generate states
        states: List[State] = []
        for i in range(self.n_states):
            is_final = random.random() < self.final_ratio
            state = State(name=f"q{i}", is_Final=is_final)
            states.append(state)

        # Generate ranked symbols
        alphabet: List[Ranked_Symbol] = []
        for i in range(self.n_symbols):
            rank = random.randint(0, self.max_rank)
            symbol = Ranked_Symbol(name=f"f{i}", rank=rank)
            alphabet.append(symbol)

        # Generate transition rules
        transitions: List[ranked_Rule] = []
        for _ in range(self.n_rules):
            symbol = random.choice(alphabet)
            input_states = random.choices(states, k=symbol.rank)
            output_state = random.choice(states)
            rule = ranked_Rule(func=symbol)
            rule.input_states = input_states
            rule.output_state = output_state
            transitions.append(rule)

        # Create and return the ranked FTA
        return ranked_Fta(fta_name=self.fta_name, alphabet=alphabet, fta_states=states, transitions=transitions)


# Example usage
if __name__ == "__main__":
    generator = RandomRankedFtaGenerator(
    n_states=6,
    n_symbols=4,
    max_rank=2,
    n_rules=15,
    seed=42
)
    random_fta = generator.generate()
    random_fta.print_Fta()