# This class defines elements for the tropical semi ring (R\cup{\infinity}, \oplus, \otimes)

from element import Element
import math

class tropical_Element(Element):
    def __init__(self):
        super().__init__()
        self.__tr = 0           #Tropical element

    def get_tr_element(self):   #Get the real value of the tropical element
        return(self.__tr)
    
    def set_tr_element(self, e):    #set a value for the tropical element
        self.__tr = e

    def __add__(self,e):            #define the plus operator for trppical elements
        a=tropical_Element()
        a.set_tr_element(min(self.__tr,e.get_tr_element()))
        return(a)
    
    def __mul__(self,e):            #define the multiple operator for trppical elements
        a=tropical_Element()
        a.set_tr_element(self.__tr+e.get_tr_element())
        return(a)
    
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
