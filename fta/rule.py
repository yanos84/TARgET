from abc import ABC, abstractmethod

class Rule(ABC):

    @abstractmethod
    def __init__(self):
        self._input
        self._output