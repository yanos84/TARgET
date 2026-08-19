from .semiring import Semiring

class BooleanSemiring(Semiring):
    """A semiring where the elements are boolean values (True and False) and the operations are defined as follows:
    - Addition (⊕): Logical OR (∨)
    - Multiplication (⊗): Logical AND (∧)
    The zero element is False and the one element is True.
    """

    def __init__(self, value: bool):
        self.value = bool(value)

    def __add__(self, other):
        if not isinstance(other, BooleanSemiring):
            return NotImplemented
        return BooleanSemiring(self.value or other.value)

    def __mul__(self, other):
        if not isinstance(other, BooleanSemiring):
            return NotImplemented
        return BooleanSemiring(self.value and other.value)

    @classmethod
    def zero(cls):
        return cls(False)

    @classmethod
    def one(cls):
        return cls(True)

    def __repr__(self):
        return f"𝔹({self.value})"

    def __eq__(self, other):
        if not isinstance(other, BooleanSemiring):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
    

if __name__ == "__main__":
    # Example usage
    a = BooleanSemiring(True)
    b = BooleanSemiring(False)
    print(a + b)          # 𝔹(True  )   
    print(a * b)          # 𝔹(False)
    print(BooleanSemiring.zero())  # 𝔹(False)
    print(BooleanSemiring.one())   # 𝔹(True)


