from typing import Dict, Any, List
from .base import BaseReport
from ..models.process import ProcessInfo


class ProcessStatusReport(BaseReport):
    """Report generator for process status"""

    def __init__(self, exporter, show_served: bool = True):
        super().__init__(exporter)
        self.show_served = show_served

    def generate(self, data: Dict[str, Any]) -> None:
        processes = data['served_processes'] if self.show_served else data['unserved_processes']
        process_type = "served" if self.show_served else "unserved"

        header = f"Process Status Report: {process_type.capitalize()} Business Processes"
        self.exporter.export_data(
            header=header,
            data=self._format_processes(processes),
            columns=['Process Name', 'Serving Component'] if self.show_served else ['Process Name']
        )

    def _format_processes(self, processes: List[ProcessInfo]) -> List[Dict[str, str]]:
        """Format processes for export"""
        return [
            {'Process Name': p.name, 'Serving Component': p.serving_component}
            if self.show_served else
            {'Process Name': p.name}
            for p in sorted(processes, key=lambda x: x.name)
        ]
