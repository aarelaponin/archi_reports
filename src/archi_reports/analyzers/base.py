from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAnalyzer(ABC):
    """Base class for all analyzers"""

    @abstractmethod
    def parse_model(self) -> None:
        """Parse the input model into internal representation"""
        pass

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Analyze the model and return results"""
        pass
