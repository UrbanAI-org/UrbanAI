from abc import ABC, abstractmethod
class Optimizer(ABC):
    
    @abstractmethod
    def is_already_optimized(self):
        pass 

    @abstractmethod
    def execute(self):
        pass