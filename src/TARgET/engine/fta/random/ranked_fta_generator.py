import random
from typing import List
from TARgET.core.fta.rankedfta import ranked_Fta
from TARgET.core.fta.state import State
from TARgET.core.base.symbol import Ranked_Symbol
from TARgET.core.fta.rankedRule import ranked_Rule
from .randomGenerator import FtaGenerator



class RandomRankedFtaGenerator(FtaGenerator):
    """Class to generate random ranked finite tree automata (RFTAs).
    This class provides functionality to create random RFTAs based on specified parameters such as the number of states, symbols, maximum rank, and transition rules. The generated RFTAs can be used
    for testing, experimentation, or as examples for various operations on RFTAs. The generator allows for customization of the generated automata to suit different needs and scenarios.
    Attributes:
- fta_name: Name of the generated FTA.
- n_states: Number of states in the generated FTA.
- n_symbols: Number of ranked symbols in the alphabet of the generated FTA.
- max_rank: Maximum rank for the ranked symbols in the generated FTA.
- n_rules: Number of transition rules in the generated FTA.
- final_ratio: Ratio of final states among all states in the generated FTA.
- seed: Optional seed for random number generation to ensure reproducibility.
    Methods:
    - __init__: Initializes the RandomRankedFtaGenerator class with specified parameters.
    - generate: Generates a random ranked finite tree automaton (RFTA) based on the initialized parameters and returns it as an instance of ranked_Fta.
    """

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
        Generate a random ranked finite tree automaton (FTA).

        :param fta_name: The name of the generated automaton.
        :param n_states: The number of states in the automaton.
        :param n_symbols: The number of ranked symbols in the alphabet.
        :param max_rank: The maximum rank of the alphabet symbols.
        :param n_rules: The number of transition rules to generate.
        :param final_ratio: The ratio of final states among all states.

        :returns: A randomly generated ranked finite tree automaton.
        :rtype: ranked_Fta
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