from abc import ABC, abstractmethod

class abs_minimize(ABC):
    @abstractmethod
    def minimize(self, fta):
        pass
