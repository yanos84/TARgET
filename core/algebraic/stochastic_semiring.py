from .semiring import Semiring

class ProbabilitySemiring(Semiring):
    """
    Stochastic / probability semiring ([0,1], +, ×, 0, 1)
    1. Addition (+) is standard real number addition
    2. Multiplication (×) is standard real number multiplication
    3. Additive identity (0) is the real number 0.0
    4. Multiplicative identity (1) is the real number 1.0
    5. Zero is absorbing for multiplication
    6. Closure, associativity, and distributivity properties hold
    7. Commutativity of addition holds
    8. No additive inverses (not a ring)
    9. All elements are in the range [0,1], representing probabilities
    """

    def __init__(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("Probability must be in [0,1]")
        self.value = float(value)

    def __add__(self, other):
        if not isinstance(other, ProbabilitySemiring):
            return NotImplemented
        return ProbabilitySemiring(self.value + other.value)

    def __mul__(self, other):
        if not isinstance(other, ProbabilitySemiring):
            return NotImplemented
        return ProbabilitySemiring(self.value * other.value)

    @classmethod
    def zero(cls):
        return cls(0.0)

    @classmethod
    def one(cls):
        return cls(1.0)

    def __repr__(self):
        return f"𝔓({self.value:.4f})"
    
    def __str__(self):
        return f"𝔓({self.value:.4f})"
    



#Example usage 
if __name__ == "__main__":
    p1 = ProbabilitySemiring(0.3)
    p2 = ProbabilitySemiring(0.5)

    print(p1 + p2)  # 𝔓(0.8000)
    print(p1 * p2)  # 𝔓(0.1500)
