from abc import ABC, abstractmethod
from typing import Any, Dict
from ..exporters.base import BaseExporter


class BaseReport(ABC):
    """Base class for all reports"""

    def __init__(self, exporter: BaseExporter):
        self.exporter = exporter

    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> None:
        """Generate the report using the provided data"""
        pass