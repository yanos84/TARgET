# This is the abstract class monoid from which all algebric structures should inhereit

from abc import ABC, abstractmethod

class Monoid(ABC):

	@abstractmethod
	def __add__(self):
		pass
	@abstractmethod
	def __mul__(self):
		pass
	@abstractmethod
	def get_identity(self):
		pass
	@abstractmethod
	def get_absorbing(self):
		pass
