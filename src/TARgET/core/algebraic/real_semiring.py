from .semiring import Semiring

class RealSemiring(Semiring):

    """
    Represents the semiring of real numbers (ℝ, +, *, 0, 1)
    1. Addition (+) is standard real number addition
    2. Multiplication (*) is standard real number multiplication
    3. Additive identity (0) is the real number 0.0
    4. Multiplicative identity (1) is the real number 1.0
    5. Zero is absorbing for multiplication 
    6. Closure, associativity, and distributivity properties hold
    7. Commutativity of addition holds
    8. No additive inverses (not a ring)
    """

    def __init__(self, value: float):
        self.value = float(value)

    def __add__(self, other):
        if not isinstance(other, RealSemiring):
            return NotImplemented
        return RealSemiring(self.value + other.value)

    def __mul__(self, other):
        if not isinstance(other, RealSemiring):
            return NotImplemented
        return RealSemiring(self.value * other.value)

    @classmethod
    def zero(cls):
        return cls(0.0)

    @classmethod
    def one(cls):
        return cls(1.0)

    def __eq__(self, other):
        if not isinstance(other, RealSemiring):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"ℝ({self.value})"
    
# Example usage

if __name__ == "__main__": 
    a = RealSemiring(3.5)
    b = RealSemiring(2.5)   
    print(a + b)          # ℝ(6.0)
    print(a * b)          # ℝ(8.75)
    print(RealSemiring.zero())  # ℝ(0.0)
    print(RealSemiring.one())   # ℝ(1.0)
    print(RealSemiring(4.2))  # ℝ(4.2)