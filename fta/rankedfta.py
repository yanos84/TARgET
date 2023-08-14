# impmlementation of ranked finite tree automata

from fta import Fta
from state import State

class ranked_Fta(Fta):

    #Define constructor

    def __init__(self, fta_name=None, fta_states=[]):
        super().__init__(fta_name,fta_states)



r= ranked_Fta("new fta")
print(r.name) 
r.name="updating its name"
print(r.name) 
print(r.states_list) 
st = State(name="olivier",final=False, init=False)
print(st.name, st.is_Final)
r.add_state(st)
print(r.states_list) 
