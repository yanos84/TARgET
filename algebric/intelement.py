# implements an integer element used in semiring of integers N(+,*,1,0)

from element import Element

class Int_element(Element):
    def __init__(self):
        self.__i=0             # creates a interger i as element

    def set_Value(self,a):     #gives a value to i
        self.__i=a
    
    def get_Value(self):       #returnes the value of i
        return(self.__i)

    def __add__(self,j):       # override the add to accept int_elements
        return self.__i + j.get_Value()
    
        
#integer = Int_element()
#print(integer+Int_element())