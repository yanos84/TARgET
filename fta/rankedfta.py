# impmlementation of ranked finite tree automata
# The class imports ranked alphabets and ascendent rules. On can define ascendency or descendency in the acceptor engine.


from fta import Fta
from state import State
from alphabet import ranked_Alpha

class ranked_Fta(Fta):

    #Define constructor

    def __init__(self, fta_name=None, fta_states=[]):
        super().__init__(fta_name,fta_states)
        self._alphabet


"""
-------------Testing -------------------------------------------------------
"""


# r= ranked_Fta("new fta")
# print(r.name) 
# r.name="updating its name"
# print(r.name) 
# print(r.states_list) 
# st = State(name="olivier",final=False, init=False)
# print(st.name, st.is_Final)
# r.add_state(st)
# print(r.states_list) 
