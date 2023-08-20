#********The abstract class defining rules (transition functions)**************
# The user can inherit from this class in order to define more sophisticated transition rules such as transducers ...

from abc import ABC, abstractmethod

class Rule(ABC):

    @abstractmethod
    def __init__(self):
        pass