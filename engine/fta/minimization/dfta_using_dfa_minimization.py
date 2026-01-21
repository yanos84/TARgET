import libmata.nfa.nfa as mata_nfa
from engine.fta.minimization.dfta_standard_minimization import dfta_minimizer
from fta.rankedRule import ranked_Rule
from fta.rankedfta import ranked_Fta
from fta.state import State
import base64, hashlib



class dfta_using_fta_minimizer(dfta_minimizer):
    def __init__(self):
        super().__init__()
    
    def create_states_index(self, fta:ranked_Fta)->dict[str, int]:
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
        for j in range(len(rule.input_states)):
            remining = []
            remining.append(rule.func.name)
            for i in range(len(rule.input_states)):
                if i!=j:
                    remining.append(rule.input_states[i].name)
                else:
                    remining.append("#")
            serialized = "|".join(obj for obj in remining) # Serialize the structure
            unique_key = hashlib.md5(serialized.encode()).hexdigest() # Generate a unique key
            unique_key = base64.urlsafe_b64encode(unique_key.encode())[:8].decode() # Shorten the key for practicality
            store[unique_key] = remining.copy()
            fa_transitions.append( (state_index[rule.input_states[j].name], unique_key, state_index[rule.output_state.name]) ) # Add the transition. Alphabet is defined as string. It must be converted to integer when creating NFA

        return fa_transitions
    
    def create_nfa_from_fta(self, fta:ranked_Fta)->mata_nfa.Nfa:
        '''
            Create an NFA from the given deterministic FTA.

        '''
        raw_transitions=[]
        store = {}
        states_index = self.create_states_index(fta) # Map state names to indices in NFA and reserve 0 for new initial state
        for rule in fta.transitions: # For each FTA rule,  compute its horizontal language transitions (those of the NFA)
            horizontal_lang = self.create_horizontal_language(rule, store, states_index)
            raw_transitions.extend(horizontal_lang)
        alphabet_to_id = {label: idx for idx, label in enumerate(store.keys())}  # Map each unique label to a unique integer ID
        aut = mata_nfa.Nfa(len(fta.states_list)+1)  # +1 for new initial state
        aut.make_initial_state(0) # New initial state is 0
        for state in fta.states_list:
            aut.add_transition(0, states_index[state.name], states_index[state.name]) # New transitions from new initial state to old initial states just to respect NFA format
  

        final_states={states_index[state.name] for state in fta.states_list if state.is_Final}
        for state in final_states:
            aut.make_final_state(state)

        for from_state, symbol, to_state in raw_transitions:
            aut.add_transition(from_state, alphabet_to_id[symbol], to_state) # Add transition to NFA
        return aut

 


    def minimize(self, fta:ranked_Fta):
        '''
            Minimize the given deterministic FTA using NFA minimization techniques.
            Returns a new minimized DFTA.
        '''
        if not self.check_determinism(fta):
            raise ValueError("FTA must be deterministic for minimization.")
        nfa = self.create_nfa_from_fta(fta)
        if not nfa.is_deterministic():
            raise ValueError("Constructed NFA is not deterministic. But it should be.")
        min_nfa = mata_nfa.minimize(nfa)
        final_partition = self.extract_right_partition(min_nfa)
        minimized_fta = self.minimize_fta_from_partition(fta, final_partition)
        return minimized_fta

    def extract_right_partition(self, nfa:mata_nfa.Nfa, root=0):
        """
        Extracts the partition induced by minimization.

        Encoding assumed:
            root -[old_state]→ minimized_state
        """
        partition = {}

        for t in nfa.get_trans_as_sequence():
            if t.source == root:
                old_state = t.symbol
                min_state = t.target
                partition.setdefault(min_state, set()).add(old_state)

        return partition


    
    def minimize_fta_from_partition(self, fta:ranked_Fta, partition):
        """
        fta: object with attributes
            - states_list: List[State]
            - transitions: List[ranked_Rule]
            - alphabet: whatever you need
        partition: dict[min_state] -> set[original_states]

        Returns a new minimized FTA
        """

        states_index = self.create_states_index(fta)
        # Step 1: build representative map
        rep = {}
        for cls, states in partition.items():
            for q in states:
                rep[q] = cls

        # Step 2: build minimized rules
        min_states = []
        new_rules = set()
        for rule in fta.transitions:
            lhs = [State(name=str(rep[states_index[s.name]]), final=s.is_Final, init=False) for s in rule.input_states]
            min_states=list(set(min_states+lhs))
            rhs = State(name=str(rep[states_index[rule.output_state.name]]), final=rule.output_state.is_Final)  # map output state
            if rhs not in min_states:
                min_states.append(rhs)
            new_rule = ranked_Rule(
                func=rule.func,
                #_states = [State(name=str(q), final=False, init=False) for q in lhs],
                input_states=lhs,
                output_state=rhs
            )
            new_rules.add(new_rule)

        # Step 3: build minimized FTA
        

        # Final states are implicit — partition guarantees consistency

        return ranked_Fta(
            fta_states=min_states,
            alphabet=fta.alphabet,
            transitions=new_rules
        )


      
        

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
    min_fta = minimizer.minimize(fta)
    print(min_fta)

    
    #nfa.
