

class Alpha:
    def __init__(self,name):
        self._name = name
    @property 
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    

class ranked_Alpha(Alpha):
    def __init__(self, name, rank):
        super().__init__(self, name)
        self._rank = rank
    @property 
    def rank(self):
        return self._rank
    @rank.setter
    def name(self, value):
        self._rank = value