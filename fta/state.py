# This class defines states as a structure containing a string name and its nature (final, intitial or normal)
class State:
    #@abstractclassmethod
    def __init__(self,name=None,final=False, init=False):
        self._name = name
        self._is_Final = final
        self._is_Initial =  init
    
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
    def is_Final(self,value):
        self._is_Final= value
    