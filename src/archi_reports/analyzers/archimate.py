import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import Dict, Any, Tuple, List
from ..models.process import ProcessInfo
from .base import BaseAnalyzer


class ArchimateAnalyzer(BaseAnalyzer):
    """Analyzer for Archimate XML models"""

    def __init__(self, xml_content: str):
        self.xml_content = xml_content
        self.namespaces = {
            'archimate': "http://www.opengroup.org/xsd/archimate/3.0/",
            'xsi': "http://www.w3.org/2001/XMLSchema-instance"
        }
        self.elements = {}
        self.relationships = defaultdict(list)
        self.root = None
        self._register_namespaces()
        self.parse_model()

    def _register_namespaces(self):
        """Register XML namespaces"""
        ET.register_namespace('', "http://www.opengroup.org/xsd/archimate/3.0/")
        ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

    def parse_model(self) -> None:
        """Parse the XML model"""
        self.root = ET.fromstring(self.xml_content)
        self._parse_elements()
        self._parse_relationships()

    def _parse_elements(self) -> None:
        """Parse model elements"""
        for element in self.root.findall(".//archimate:elements/archimate:element", self.namespaces):
            element_type = element.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            element_id = element.get('identifier')
            name_elem = element.find('archimate:name', self.namespaces)
            element_name = name_elem.text if name_elem is not None else ''

            self.elements[element_id] = {
                'type': element_type,
                'name': element_name
            }

    def _parse_relationships(self) -> None:
        """Parse model relationships"""
        for relationship in self.root.findall(".//archimate:relationships/archimate:relationship", self.namespaces):
            source = relationship.get('source')
            target = relationship.get('target')
            rel_type = relationship.get('{http://www.w3.org/2001/XMLSchema-instance}type')

            self.relationships[target].append({
                'source': source,
                'type': rel_type
            })

    def analyze(self) -> Dict[str, Any]:
        """Analyze the model and return results"""
        served_processes, unserved_processes, app_component_services = self._analyze_processes()
        return {
            'served_processes': served_processes,
            'unserved_processes': unserved_processes,
            'app_component_services': app_component_services
        }

    def _analyze_processes(self) -> Tuple[List[ProcessInfo], List[ProcessInfo], Dict[str, List[str]]]:
        """Analyze business processes and their relationships"""
        served_processes = []
        unserved_processes = []
        app_component_services = defaultdict(list)

        for element_id, element_info in self.elements.items():
            if element_info['type'] == 'BusinessProcess':
                self._process_business_process(
                    element_id,
                    element_info,
                    served_processes,
                    unserved_processes,
                    app_component_services
                )

        return served_processes, unserved_processes, dict(app_component_services)

    def _process_business_process(
            self,
            element_id: str,
            element_info: Dict[str, str],
            served_processes: List[ProcessInfo],
            unserved_processes: List[ProcessInfo],
            app_component_services: Dict[str, List[str]]
    ) -> None:
        """Process a single business process element"""
        has_serving_relationship = False
        process_name = element_info['name']

        for rel in self.relationships[element_id]:
            source_id = rel['source']
            if (source_id in self.elements and
                    self.elements[source_id]['type'] == 'ApplicationComponent' and
                    rel['type'] == 'Serving'):
                has_serving_relationship = True
                app_component_name = self.elements[source_id]['name']
                served_processes.append(ProcessInfo(process_name, app_component_name))
                app_component_services[app_component_name].append(process_name)
                break

        if not has_serving_relationship:
            unserved_processes.append(ProcessInfo(process_name))
