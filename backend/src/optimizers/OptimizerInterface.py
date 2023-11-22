from abc import ABC, abstractmethod
class Optimizer(ABC):
    """
    Abstract base class for optimizers.
    """

    @abstractmethod
    def is_already_optimized(self):
        """
        Check if the optimizer has already been applied.

        Returns:
            bool: True if the optimizer has already been applied, False otherwise.
        """
        pass 

    @abstractmethod
    def execute(self):
        """
        Execute the optimization process.
        """
        pass