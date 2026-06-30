from TARgET.rte.rte import Rte, Plus, CProduct, CStar, Zero, One, function, Atom
from TARgET.core.symbol import Symbol, Ranked_Symbol
class Normalizer():
    """
    Abstract base class for RTE normalizers.
    Defines the interface for all basic normalizer variants.
    """
    def __init__(self):
        pass

    def normalize(self, expr: Rte) -> Rte:
        """
        Normalizes the given Rational Tree Expression (RTE).
        :param rte: The RTE to be normalized.
        :return: The normalized RTE.
        """
        if isinstance(expr, (Zero, One)):
            return expr

        if isinstance(expr, function):
            return function(expr.symbol, [self.normalize(a) for a in expr.args])

        if isinstance(expr, Plus):
            return self.normalize_plus(expr.terms)

        if isinstance(expr, CProduct):
            return self.normalize_cproduct(expr)

        if isinstance(expr, CStar):
            return self.normalize_cstar(expr.expr, expr.concat)

        if isinstance(expr, Atom):
            return expr

        raise TypeError("Unknown RTE type")

    def normalize_plus(self, terms: list[Rte]) -> Rte:
        """
        Normalizes a Plus RTE with the given terms.
        :param terms: The list of RTE terms in the Plus expression.
        :return: The normalized Plus RTE.
        """
        flat = []

        for t in terms:
            t = self.normalize(t)
            if isinstance(t, Zero):
                continue
            if isinstance(t, Plus):
                flat.extend(t.terms)
            else:
                flat.append(t)

        unique = set(flat)
        ordered = tuple(sorted(unique, key=repr))

        if not ordered:
            return Zero()
        if len(ordered) == 1:
            return ordered[0]

        return Plus(*ordered)
    
    def normalize_cproduct(self, expr: CProduct) -> Rte:
        """
        Normalizes a CProduct RTE with the given left and right expressions.
        :param expr: The CProduct RTE to be normalized.
        :return: The normalized CProduct RTE.
        """
        left = self.normalize(expr.left)
        right = self.normalize(expr.right)

        if isinstance(left, Zero) or isinstance(right, Zero):
            return Zero()

        if isinstance(left, One):
            return right

        if isinstance(right, One):
            return left

        return CProduct(left, right, expr.concat)
    
    def normalize_cstar(self, expr: Rte, concat: Symbol) -> Rte:
        """
        Normalizes a CStar RTE with the given expression and concatenation symbol.
        :param expr: The RTE to be normalized.
        :param concat: The concatenation symbol for the CStar expression.
        :return: The normalized CStar RTE.
        """
        expr = self.normalize(expr)

        if isinstance(expr, Zero):
            return One()

        if isinstance(expr, One):
            return One()

        if isinstance(expr, CStar) and expr.concat == concat:
        # (E*ₐ)*ₐ = E*ₐ
            return expr

        return CStar(expr, concat)

# Example usage
if __name__ == "__main__":
    normalizer = Normalizer()


   # symbols
    a = Ranked_Symbol("a")
    b = Ranked_Symbol("b")
    f = Ranked_Symbol("f", rank=2)
    g = Ranked_Symbol("g", rank=1)

    # RTEs
    fab = CProduct(function(f, [function(a, []), function(b, [])]), function(f, [function(a, []), function(b, [])]), concat=a)
    gx = function(g, [function(a, [])])

    # rational tree expression
    rte0 = Plus(
        CStar(fab, concat=a),
        CProduct(fab, gx, concat=a),
        CStar(fab, concat=a)
    )




    rte = Plus(
        Atom(a),
        Plus(
            Atom(a),
            Atom(b)
        )
    )

    print("Original RTE:")
    print(rte)

    normalized_rte = normalizer.normalize(rte)

    print("\nNormalized RTE:")
    print(normalized_rte)

    rte2 = Plus(
    Zero(),
    function(a, [])
)
    normalized_rte2 = normalizer.normalize(rte2)
    print("\nOriginal RTE 2:")
    print(rte2)
    print("\nNormalized RTE 2:")
    print(normalized_rte2)

    rte3 = CProduct(
    One(),
    function(b, []),
    concat=a
)
    normalized_rte3 = normalizer.normalize(rte3)
    print("\nOriginal RTE 3:")
    print(rte3)
    print("\nNormalized RTE 3:")
    print(normalized_rte3)

    rte4 = CStar(Zero(), concat=a)
    normalized_rte4 = normalizer.normalize(rte4)
    print("\nOriginal RTE 4:")
    print(rte4)
    print("\nNormalized RTE 4:")
    print(normalized_rte4)

    rte5 = CStar(
    CStar(function(a, []), concat=a),
    concat=a
)
    normalized_rte5 = normalizer.normalize(rte5)
    print("\nOriginal RTE 5:")
    print(rte5)
    print("\nNormalized RTE 5:")
    print(normalized_rte5)



