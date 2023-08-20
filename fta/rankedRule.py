from rule import Rule
from alphabet import ranked_Alpha

class ranked_Rule(Rule):
    def __init__(self, symbol=None):
        super().__init__()
        self._func= symbol
        self._input = []
        self._output

    @property
    def func(self):
        return self._func
    @func.setter
    def func(self,value):
        self._func = value
    @func.deleter
    def func(self):
        del _func

