
from operator import uniary_Operator

class unranked_Ops():
    def __init__(self, arity_symbs, star_symbs, concat_symbs):
        self.arity_symbs = []
        self.star_symbs = []
        self.concat_symbs = []
        for symb in arity_symbs:
            op = uniary_Operator(name = symb)  