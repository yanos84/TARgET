"""****Tree implementation***********"""

from typing import List

class Tree:

	"""
	A class impmlementing tree structure.

	Attributes:
		_children: List [Tree] : A list containing direct children of the class root
		data: contains the information (the symbol) of the tree's root
		_parent: Contains the parent of the tree in question 
	"""

	def __init__(self, data:str=None):

		"""
		Initialize the tree construction

		Args:
			_children: List [Tree] : A list containing direct children of the class root
			data: contains the information (the symbol) of the tree's root
			_parent: Contains the parent of the tree in question 	
		"""
		self._children = None
		self.data = data
		self._parent : Tree

	"""
    Defining setters and getters for the class attributes
    """ 
    
	@property
	def children(self):
		return self._children
	@children.setter
	def children(self, _value):
		if not isinstance(_value, list):
			raise TypeError("children must be trees")
		self._children = _value
	
	def __str__(self) -> str:
		"""
		Overriding __str__ for the object Tree

		Returns:
			str: recursively transforms the tree to string
		"""
		_str = self.data + "("
		if self.children !=None:
			for i in self.children:
				_str = _str + str(i)+","
		_str = _str[:-1]
		_str  = _str +  ")"
		return _str

	def add_Child(self, value):
		if not (isinstance(value, Tree)):
			raise TypeError("Child must be a tree")
		else:
			self.children.append(value)

"""
# Example usage

t=Tree("t")
u=Tree("u")
v=Tree("v")
w=Tree("w")
child = []
child.append(w)
v.children = child
child = []
child.append(u)
child.append(v)
t.children = child
print(t)
"""