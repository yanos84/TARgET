"""*********************This is the abstract class RTE from which all rte variantes herit.

The rational expressions are presented in their formal form. Classes like [A Z], digit ..ect are not supported.
Only the oparators +,*c, .c for trees or +, *, . for strings are taken into account.
"""

from abc import ABC, abstractmethod
import sys
sys.path.append('../TARgET')
from fta.alphabet import Alpha, ranked_Alpha

class Rte(ABC):

	"""
	A class implmenting the most general form of tree rational expression
	
	Attributes:
		expresson: The expression itself as strings
	"""
	@abstractmethod
	def __init__(self, exp = None):
		"""
		Constructor for Rte
		
		Args:
			exp: Contains a string version of the expression. 
		"""
		self.expression = exp

	@abstractmethod
	def rte_Build_Tree(self):
		"""
			This method builds a tree from the string version of the expression. It raises an exception if the expression 
			is not valid.
		"""
		pass

class ranked_Rte(Rte):
	def __init__(self, exp):
		super().__init__(exp)
		self.regex_Tree
		



"""# Example 

exp = ranked_Rte("hello")
print(exp.expression)
"""
