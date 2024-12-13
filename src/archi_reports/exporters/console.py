from typing import List, Dict, Any
from .base import BaseExporter


class ConsoleExporter(BaseExporter):
    """Exporter for console output"""

    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        print(f"\n{header}")
        print(f"Found {len(data)} items:")

        for i, item in enumerate(data, 1):
            line = f"{i}. "
            line += " - ".join(str(item[col]) for col in columns if item.get(col) is not None)
            print(line)
