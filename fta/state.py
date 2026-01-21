# This class defines states as a structure containing a string name and its nature (final, intitial or normal)
class State:
    #@abstractclassmethod
    def __init__(self,name=None,is_Final=False, is_Initial=False):
        self._name = name
        self._is_Final = is_Final
        self._is_Initial =  is_Initial
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name= value
         
    @property
    def is_Final(self):
        return self._is_Final
    @is_Final.setter
    def is_Final(self,value:bool):
        self._is_Final= value
    
    @property
    def is_Initial(self):
        return self._is_Initial
    @is_Final.setter
    def is_Final(self,value:bool):
        self._is_Final= value

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)