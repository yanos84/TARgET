# This is the abstract class monoid from which all algebric structures should inhereit

from abc import ABC, abstractmethod

class Monoid(ABC):
	"""
	Abstract base class for monoids.
	Some algebraic structures, such as semirings, are built upon monoids. This class defines the essential operations and properties that any monoid must implement, including addition, multiplication, identity elements, and absorbing elements. Subclasses of Monoid should provide concrete implementations of these methods to define specific algebraic structures.	
	"""

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
