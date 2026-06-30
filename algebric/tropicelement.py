# This class defines elements for the tropical semi ring (R\cup{\infinity}, \oplus, \otimes)

from TARgET.algebric.element import Element
import math

class tropical_Element(Element):
    """
    Represents an element in the tropical semiring.
    This class provides methods for setting and getting the value of the tropical element, as well as overriding the addition and multiplication operators to allow for operations on tropical elements. The tropical semiring is defined with the following operations:
        1. Addition (⊕) is defined as minimum: a ⊕ b = min(a, b)
        2. Multiplication (⊗) is defined as standard addition: a ⊗ b = a + b
        3. Additive identity (∞) is positive infinity
        4. Multiplicative identity (0) is the real number 0.0
        5. Zero (∞) is absorbing for multiplication
        6. Closure, associativity, and distributivity properties hold
        7. Commutativity of addition holds
        8. No additive inverses (not a ring)
    """
    def __init__(self,a):
        super().__init__()
        self.__tr = a           #Tropical element

    def get_tr_element(self):   #Get the real value of the tropical element
        return(self.__tr)
    
    def set_tr_element(self, e):    #set a value for the tropical element
        self.__tr = e

    def __add__(self,e):            #define the plus operator for trppical elements
        return(tropical_Element(min(self.__tr,e.get_tr_element())))
    
    def __mul__(self,e):            #define the multiple operator for trppical elements
        return(tropical_Element(self.__tr+e.get_tr_element()))
    
    def get_identity(self):   #put infinity as neutral element for the oplus operator
        return (math.inf)
    
        

#-------------Testing-----------------------------------------------------------------------
# alpha = tropical_Element()
# alpha.set_tr_element(5)
# beta = tropical_Element()
# beta.set_tr_element(3)
# gamma=alpha+beta
# print(gamma.get_tr_element())
# gamma=alpha*beta
# print(gamma.get_tr_element())
# print(alpha.get_identity())
