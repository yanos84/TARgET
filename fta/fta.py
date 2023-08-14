#This is the abstract class FTA from which all tree automata variantes should inherit.

from abc import ABC, abstractmethod

class Fta(ABC):

	@abstractmethod
	def __init__(self, fta_name, fta_states):
		self._name = fta_name
		self._states = []
		self._states.append(fta_states)
