from abc import ABC, abstractmethod

class Semiring(ABC):
    """
    Abstract base class for semirings:
    (S, +, *, 0, 1)
        1. Addition (+) is associative and commutative
        2. Multiplication (*) is associative
        3. Additive identity (0) exists
        4. Multiplicative identity (1) exists
        5. Zero (0) is absorbing for multiplication
        6. Distributivity of multiplication over addition holds
        7. No additive inverses (not a ring)
        8. Closure property holds for both operations
        9. Commutativity of addition holds
        10. Examples include natural numbers, Boolean algebra, tropical semiring, etc.  
    """

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @classmethod
    @abstractmethod
    def zero(cls):
        """Additive identity"""
        pass

    @classmethod
    @abstractmethod
    def one(cls):
        """Multiplicative identity"""
        pass

    @classmethod
    def absorbing(cls):
        """By default, zero is absorbing"""
        return cls.zero()
