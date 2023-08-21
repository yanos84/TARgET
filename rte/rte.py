#This is the abstract class RTE from which all rte variantes herit.

from abc import ABC, abstractmethod

class Rte(ABC):
	@abstractmethod
	def __init__(self, exp = None):
		self.expression = exp

class ranked_Rte(Rte):
	def __init__(self, exp):
		super().__init__(exp)



# Example 

exp = ranked_Rte("hello")
print(exp.expression)

