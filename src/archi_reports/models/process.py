from dataclasses import dataclass
from typing import Optional


@dataclass
class ProcessInfo:
    """Data class to store process information"""
    name: str
    serving_component: Optional[str] = None
