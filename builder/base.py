# builder/base.py
from abc import ABC, abstractmethod

class Step(ABC):
    @abstractmethod
    def execute(self, context: dict):
        """Execute this step."""
        pass
