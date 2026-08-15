# This class defines states as a structure containing a string name and its nature (final, intitial or normal)
class State:


    """
    Represents a state in a finite tree automaton (FTA) with a name and properties indicating whether it is a final or initial state.
    Attributes:
        name (str): The name of the state.
        is_Final (bool): Indicates whether the state is a final state (default is False).
        is_Initial (bool): Indicates whether the state is an initial state (default is False).
    Methods:
        __init__: Initializes a State object with a name and optional final and initial properties.
        name: Property to get or set the name of the state.
        is_Final: Property to get or set whether the state is a final state.
        is_Initial: Property to get or set whether the state is an initial state.
    """
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
    @is_Initial.setter
    def is_Initial(self, value: bool):
        self._is_Initial = value

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

# ____example of usage____
if __name__ == "__main__":
    q= State(name="q", is_Final=False, is_Initial=False)
    q.is_Initial = True  # Set the state as initial
    print(q.name)  # Output: q
    print(q.is_Final)  # Output: False
    print(q.is_Initial)  # Output: True