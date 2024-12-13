import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from .base import BaseExporter


class CsvExporter(BaseExporter):
    """Exporter for CSV files"""

    def __init__(self, report_type: str):
        self.report_type = report_type

    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        os.makedirs('reports', exist_ok=True)
        filename = f"reports/{self.report_type}_{datetime.now():%Y%m%d_%H%M%S}.csv"

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
