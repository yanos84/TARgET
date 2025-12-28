import math
from semiring import Semiring

class TropicalSemiring(Semiring):
    '''
    Docstring for TropicalSemiring
    Represents the tropical semiring (𝕋, ⊕, ⊗, ∞, 0)
    1. Addition (⊕) is defined as minimum: a ⊕ b    = min(a, b)
    2. Multiplication (⊗) is defined as standard addition: a ⊗ b = a + b
    3. Additive identity (∞) is positive infinity
    4. Multiplicative identity (0) is the real number 0.0
    5. Zero (∞) is absorbing for multiplication 
    6. Closure, associativity, and distributivity properties hold
    7. Commutativity of addition holds
    8. No additive inverses (not a ring)
    '''

    def __init__(self, value: float):
        self.value = float(value)

    def __add__(self, other):
        if not isinstance(other, TropicalSemiring):
            return NotImplemented
        return TropicalSemiring(min(self.value, other.value))

    def __mul__(self, other):
        if not isinstance(other, TropicalSemiring):
            return NotImplemented
        return TropicalSemiring(self.value + other.value)

    @classmethod
    def zero(cls):
        return cls(math.inf)

    @classmethod
    def one(cls):
        return cls(0.0)

    def __repr__(self):
        if self.value == math.inf:
            return "𝕋(∞)"
        return f"𝕋({self.value})"

# Example usage
a = TropicalSemiring(3.0)
b = TropicalSemiring(5.0)
print(a + b)          # 𝕋(3.0   )   
print(a * b)          # 𝕋(8.0   )
print(TropicalSemiring.zero())  # 𝕋(∞)
print(TropicalSemiring.one())   # 𝕋(0.0 )

