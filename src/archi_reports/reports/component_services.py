from typing import Dict, Any, List
from .base import BaseReport


class ComponentServicesReport(BaseReport):
    """Report generator for component services"""

    def generate(self, data: Dict[str, Any]) -> None:
        app_component_services = data['app_component_services']

        formatted_data = []
        for app_component, processes in sorted(app_component_services.items()):
            for process in sorted(processes):
                formatted_data.append({
                    'Application Component': app_component,
                    'Process Name': process
                })

        self.exporter.export_data(
            header="Application Components and Their Served Processes",
            data=formatted_data,
            columns=['Application Component', 'Process Name']
        )
