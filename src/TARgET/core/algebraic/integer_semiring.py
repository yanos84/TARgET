from .semiring import Semiring

class IntegerSemiring(Semiring):

    """
        Represents the semiring of integers (ℤ, +, *, 0, 1)
        1. Addition (+) is standard integer addition
        2. Multiplication (*) is standard integer multiplication
        3. Additive identity (0) is the integer 0
        4. Multiplicative identity (1) is the integer 1
        5. Zero is absorbing for multiplication 
        6. Closure, associativity, and distributivity properties hold
        7. Commutativity of addition holds
        8. No additive inverses (not a ring)    
    """

    def __init__(self, value: int):
        self.value = int(value)

    def __add__(self, other):
        if not isinstance(other, IntegerSemiring):
            return NotImplemented
        return IntegerSemiring(self.value + other.value)

    def __mul__(self, other):
        if not isinstance(other, IntegerSemiring):
            return NotImplemented
        return IntegerSemiring(self.value * other.value)

    @classmethod
    # Additive identity
    def zero(cls):
        return cls(0)

    @classmethod
    # Multiplicative identity
    def one(cls):
        return cls(1)

    def __eq__(self, other):
        # Equality check
        return isinstance(other, IntegerSemiring) and self.value == other.value
    def __eq__(self, other):
        if not isinstance(other, IntegerSemiring):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        # String representation
        return f"ℤ({self.value})"
    

if __name__ == "__main__":
    # Example usage     

    a = IntegerSemiring(3)
    b = IntegerSemiring(5)

    print(a + b)          # ℤ(8)
    print(a * b)          # ℤ(15)
    print(IntegerSemiring(4))
    print(IntegerSemiring.zero())  # ℤ(0)
    print(IntegerSemiring.one())   # ℤ(1)
