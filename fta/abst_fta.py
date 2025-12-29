"""
******************This is the abstract class FTA from which all tree automata variantes should inherit*****************


 It contains the name of the automaton, the list of its states. Despite the fact that the ascendent and the descendent 
 rules can be written similarly, we avoid to declare the rules in the Fta class to allow the user to define more 
 elaborate Fta types like transducers and weighed automata.

"""

from abc import ABC, abstractmethod
from .state import State
from typing import List

class Fta(ABC):
	"""
	An abstract class defining finite tree automata. All tree automata inherits directly or indirectly from Fta

	Attributes:
		_name: contains conventional fta name
		_states: The list of fta states

	"""

	@abstractmethod
	def __init__(self, fta_name, fta_states):
		self._name = fta_name
		self._states : List[State]
		self._states = fta_states
	

	#@abstractmethod
	def add_state(self,s_name):
		if s_name not in self._states:
			self._states.append(s_name)
		else:
			raise Exception("no duplicated states are allowed")
		
	def remove_from_states(self, s_name):
		self._states.remove(s_name)

	"""
    *** Define setters, getters and deletters for :
            name,
            states list
    """
    
	@property
	def states_list(self):
		return self._states
    
	@states_list.setter
	def states_list(self, value):
		self._states = value
	#@states_list.deleter
	#def states_list(self):
	#	del self._states

	@property
	def name(self):
		return self._name
    
	@name.setter
	def name(self, value):
		self._name = value
    
	#@name.deleter
	#def name(self):
	#	   del self._name

	



	
# 	@abstractmethod

# def add_state(self,s_name):
# 		if s_name not in self._states:
#             self._states.append(s_name)
# 		else:
# 			raise Exception("No duplicated states names are allowed")			
	

    # **** add_state adds a state to an the states list if it is not present already

    