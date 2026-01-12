import libmata.nfa.nfa as mata_nfa
from engine.fta.minimization.dfta_standard_minimization import dfta_minimizer
from fta.rankedRule import ranked_Rule
import base64, hashlib


class dfta_using_fta_minimizer(dfta_minimizer):
    def __init__(self):
        super().__init__()
    
    def create_states_index(self, fta)->dict[str, int]:
        ''' Create a mapping from state names to their indices in the FTA's state list. '''
        state_index = {}
        for idx, state in enumerate(fta.states_list):
            state_index[state.name] = idx+1  # +1 to reserve 0 for new initial state  
        return state_index

    def create_horizontal_language(self, rule:ranked_Rule, store, state_index:dict)->list:
        ''' 
            Create horizontal language transitions for a given FTA rule.
             Each transition is represented as a tuple (from_state, symbol, to_state).
            '''
        fa_transitions = []
        for j in range(len(rule.input)):
            remining = []
            remining.append(rule.func.name)
            for i in range(len(rule.input)):
                if i!=j:
                    remining.append(rule.input[i].name)
                else:
                    remining.append("#")
            serialized = "|".join(obj for obj in remining) # Serialize the structure
            unique_key = hashlib.md5(serialized.encode()).hexdigest() # Generate a unique key
            unique_key = base64.urlsafe_b64encode(unique_key.encode())[:8].decode() # Shorten the key for practicality
            store[unique_key] = remining.copy()
            fa_transitions.append( (state_index[rule.input[j].name], unique_key, state_index[rule.output.name]) ) # Add the transition. Alphabet is defined as string. It must be converted to integer when creating NFA

        return fa_transitions
    
    def create_nfa_from_fta(self, fta)->mata_nfa.Nfa:
        raw_transitions=[]
        store = {}
        states_index = self.create_states_index(fta)
        print(states_index)
        for rule in fta.transitions:
            horizontal_lang = self.create_horizontal_language(rule, store, states_index)
            raw_transitions.extend(horizontal_lang)
        alphabet_to_id = {label: idx for idx, label in enumerate(store.keys())}  # Map each unique label to a unique integer ID
        print(store)
        aut = mata_nfa.Nfa(len(fta.states_list)+1)
        
        #init = len(fta.states_list)  # New initial state index
        print("Initial state:", 0)
        aut.make_initial_state(0)
        for state in fta.states_list:
            aut.add_transition(0, states_index[state.name], states_index[state.name])
            print(f"Added transition from initial state {0} to state {states_index[state.name]}")

        final_states={states_index[state.name] for state in fta.states_list if state.is_Final}
        print("Final states:", final_states)
        sink_alphabet = len(alphabet_to_id)
        for state in final_states:
            aut.make_final_state(state)
            print(f"Made state {state} final")
            #aut.add_transition(state, sink_alphabet+j, state)



        for from_state, symbol, to_state in raw_transitions:
            aut.add_transition(from_state, alphabet_to_id[symbol], to_state)
        return aut



    def minimize(self, fta):
        if not self.check_determinism(fta):
            raise ValueError("FTA must be deterministic for minimization.")
        nfa = self.create_nfa_from_fta(fta)
        if not nfa.is_deterministic():
            raise ValueError("Constructed NFA is not deterministic. But it should be.")
        print(nfa)
        return mata_nfa.minimize(nfa)
        
        

if __name__ == "__main__":
    from engine.utils.rankedFta_xml_import import load_fta_from_xml
    fta = load_fta_from_xml("dfta_for_minim.xml")

    print("Original FTA:")
    fta.print_Fta()
    minimizer = dfta_using_fta_minimizer()
    #states_index = minimizer.create_states_index(fta)
    #store = {}
    #print(minimizer.create_horizontal_language(r3, store, states_index))
    #print(store)
    #nfa = minimizer.create_nfa_from_fta(fta)
    #print(nfa)
    #print(nfa.is_deterministic())
    nfa = minimizer.minimize(fta)
    print(nfa)
    print(nfa.is_deterministic())
    
    #nfa.
