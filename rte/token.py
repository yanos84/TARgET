
import re

class token:
    pass

class token_rankedRte(token):
    def __init__(self, exp:str):
        self._operators = [ ('STAR', r'*.'),('ARITY', r'.(*)'), ('PLUS', r'+'), ('CONCAT', r'\. .')]
        self._exp =exp

    def find_Operators(self):
        return (re.search("*.'", self._exp))
    
tok = token_rankedRte("f(a*c)")
#print(tok.find_Operators())
print(re.search(r'\*.',"f(a*c)"))