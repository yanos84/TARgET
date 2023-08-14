# impmlementation of ranked finite tree automata

from fta import Fta

class ranked_Fta(Fta):

    #Define constructor

    def __init__(self, fta_name=None, fta_states=[]):
        super().__init__(fta_name,fta_states)

    """
    *** Define setters, getters and deletters for :
            name,
            states list
    """
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @name.deleter
    def name(self):
        del self._name
        
    @property
    def states_list(self):
        return self._states
    
    @states_list.setter
    def states_list(self, value):
        self._states = value
    
    @states_list.deleter
    def states_list(self):
        del self._states

    # **** add_state adds a state to an the states list if it is not present already

    def add_state(self,s_name):
        if s_name not in self._states:
            self._states.append(s_name)
        else:
            raise Exception("No duplicated states names are allowed")

r= ranked_Fta("new fta", "states list hi")
print(r.name) 
r.name="updating its name"
print(r.name) 
print(r.states_list) 
r.add_state("hello")
print(r.states_list) 
r.add_state("hello")
print(r.states_list)