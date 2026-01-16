import random
from typing import Sequence
from rte.rte import Rte, Symbol, Zero, One, Plus, CProduct, CStar, function, Atom
from core.symbol import Symbol, Ranked_Symbol  

class RandomRteGenerator:
    def __init__(
        self,
        symbols: Sequence[Symbol],
        concat_symbols: Sequence[Symbol],
        max_depth: int = 4,
        p_zero: float = 0.05,
        p_one: float = 0.05,
        p_function: float = 0.35,
        p_plus: float = 0.15,
        p_cproduct: float = 0.20,
        p_cstar: float = 0.10,
        p_atom: float = 0.10,
        max_plus_arity: int = 3,
        max_unranked_arity = 3
    ):
        
        if sum(1 for s in symbols if isinstance(s, Ranked_Symbol)) != len(symbols):
            raise RuntimeError("All symbols must be defined as Symbol or as Ranked_Symbol")

        self.symbols = list(symbols)
        self.concat_symbols = list(concat_symbols)
        self.max_depth = max_depth
        self.max_plus_arity = max_plus_arity
        self.max_unranked_arity = max_unranked_arity

        # normalize probabilities
        self.choices = [
            ("zero", p_zero),
            ("one", p_one),
            ("function", p_function),
            ("plus", p_plus),
            ("cproduct", p_cproduct),
            ("cstar", p_cstar),
            ("atom", p_atom)
        ]

    # --------------------------------------------------

    def generate(self, depth: int | None = None) -> Rte:
        if depth is None:
            depth = self.max_depth

        if depth == 0:
            return self._generate_base()

        kind = self._choose_kind()
        match kind:
            case "zero":
                return Zero()
            case "one":
                return One()
            case "function":
                return self._generate_function(depth)
            case "plus":
                return self._generate_plus(depth)
            case "cproduct":
                return self._generate_cproduct(depth)
            case "cstar":
                return self._generate_cstar(depth)
            case "atom":
                return self._generate_base()

        raise RuntimeError("Unknown RTE kind")

    # --------------------------------------------------

    def _generate_base(self) -> Rte:
        # only rank-0 symbols allowed
        ranked_symbs = [s for s in self.symbols if isinstance(s, Ranked_Symbol)]
        if len(ranked_symbs) == 0:
            leaf_symbols = self.symbols
        else:
            leaf_symbols = [s for s in self.symbols if s.rank == 0]
        
        if len(leaf_symbols)==0:
            raise RuntimeError("At least one ranked symbol must be of rank = 0")

        """choice = random.choice(["zero", "one", "function", "atom"])
        if choice == "zero":
            return Zero()
        if choice == "one":
            return One()
        if not leaf_symbols:
            return Zero()"""
        sym = random.choice(leaf_symbols)
        return Atom(sym)

    # --------------------------------------------------

    def _generate_function(self, depth: int) -> Rte:
        sym = random.choice(self.symbols)
        if isinstance(sym, Ranked_Symbol):
            if sym.rank == 0:
                return Atom(sym)
            else:
                args = [self.generate(depth - 1) for _ in range(sym.rank)]
                return function(sym, args)
        else:
            args = [self.generate(depth -1) for _ in range(self.max_unranked_arity)]

    # --------------------------------------------------

    def _generate_plus(self, depth: int) -> Rte:
        arity = random.randint(2, self.max_plus_arity)
        terms = [self.generate(depth - 1) for _ in range(arity)]
        return Plus(*terms)

    # --------------------------------------------------

    def _generate_cproduct(self, depth: int) -> Rte:
        concat = random.choice(self.concat_symbols)
        left = self.generate(depth - 1)
        right = self.generate(depth - 1)
        return CProduct(left, right, concat)

    # --------------------------------------------------

    def _generate_cstar(self, depth: int) -> Rte:
        concat = random.choice(self.concat_symbols)
        expr = self.generate(depth - 1)
        return CStar(expr, concat)

    # --------------------------------------------------

    def _choose_kind(self) -> str:
        kinds, weights = zip(*self.choices)
        return random.choices(kinds, weights=weights, k=1)[0]


#example usage

if __name__ == "__main__":
    a = Ranked_Symbol("a")
    b = Ranked_Symbol("b")
    #x = Ranked_Symbol("x")
    f = Ranked_Symbol("f", 2)
    g = Ranked_Symbol("g", 1)

    gen = RandomRteGenerator(
        symbols=[a, b, f, g],
        concat_symbols=[a, b],
        max_depth=4
    )

    for i in range(5):
        rte = gen.generate()
        print(rte)