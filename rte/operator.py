"""
***************Operator class************************************************************

Operator class allows us to define regular expression operators. This allows the user to set up regular tree expressions. 
For instance, one can define arity operator f(exp) as a unary one. The *c can then be defined alsor as unary one. + and .c are binary.
"""

from abc import ABC, abstractmethod
from rte import Rte

class Operator(ABC):
    
    @abstractmethod
    def __init__(self, name):
        self._name = name 
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value


class uniary_Operator(Operator):
    def __init__(self, name,arg1):
        super().__init__(name)
        self.exp :Rte = arg1

class binary_Operator(Operator):
    def __init__(self, arg1, arg2):
        super().__init__()
        self.exp1 :Rte = arg1
        self.exp2 :Rte = arg2


"""#Example usage:

ope = uniary_Operator(name = "arity", arg1 = "f(xxx)")
print(ope.name)
print(ope.exp)
"""