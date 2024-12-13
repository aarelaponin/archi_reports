from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseExporter(ABC):
    """Base class for all exporters"""

    @abstractmethod
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        """Export data in the specific format"""
        pass
