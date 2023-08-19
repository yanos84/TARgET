# defines the alphabet class. It is a simple class that allows to use basic automata and expressions. More elaborated alphabet classes should be defined in the alphabet package
# All symbolic alphabets inherit from the Alpha class. It only has a name that plays the role of the symbol itself.

class Alpha:
    def __init__(self,name):
        self._name = name
    
    # The only property of this class is the symbol's name
    @property 
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    

# A ranked (garded) symbol is an alphabet with a function (randk) that indicate the number of its children. A ranked tree can be defined in the tree package
class ranked_Alpha(Alpha):
    def __init__(self, name, rank):
        super().__init__(self, name)
        self._rank = rank

    # The property rank is added to the class
    @property 
    def rank(self):
        return self._rank
    @rank.setter
    def name(self, value):
        self._rank = value