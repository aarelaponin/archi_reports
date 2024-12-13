# Developer Manual: Adding New Reports to Archimate Analyzer

## Overview
This manual explains how to add new report types to the Archimate Analyzer system. The system is designed to be modular and extensible, allowing developers to easily add new report types without modifying existing code.

## Step-by-Step Guide

### 1. Create a New Report Class
First, create a new Python file in the `src/archi_reports/reports/` directory. Name it according to your report type (e.g., `application_usage.py` for an application usage report).

```python
# src/archi_reports/reports/application_usage.py
from typing import Dict, Any
from .base import BaseReport

class ApplicationUsageReport(BaseReport):
    """Report generator for application usage analysis"""
    
    def __init__(self, exporter):
        super().__init__(exporter)
    
    def generate(self, data: Dict[str, Any]) -> None:
        # 1. Process the data for your report
        applications = self._process_applications(data)
        
        # 2. Format the data for export
        formatted_data = self._format_data(applications)
        
        # 3. Use the exporter to output the data
        self.exporter.export_data(
            header="Application Usage Analysis",
            data=formatted_data,
            columns=['Application', 'Usage Count', 'Processes']
        )
    
    def _process_applications(self, data):
        # Your data processing logic here
        pass
    
    def _format_data(self, applications):
        # Your data formatting logic here
        pass
```

### 2. Update the Main Script
Modify `main.py` to include your new report option:

```python
parser.add_argument(
    '--report',
    type=int,
    choices=[1, 2, 3],  # Add your new report number
    default=1,
    help='''Report type: 
        1=Processes by served/unserved status, 
        2=Application Components with their served processes,
        3=Application Usage Analysis'''  # Add description for your report
)

# In the report selection section:
if args.report == 1:
    report_generator = ProcessStatusReport(exporter, show_served=args.served)
elif args.report == 2:
    report_generator = ComponentServicesReport(exporter)
elif args.report == 3:  # Add your report
    report_generator = ApplicationUsageReport(exporter)
```

### 3. Add Required Analyzer Methods (if needed)
If your report needs additional data that isn't currently being analyzed, extend the `ArchimateAnalyzer` class:

```python
# src/archi_reports/analyzers/archimate.py
class ArchimateAnalyzer(BaseAnalyzer):
    def analyze(self) -> Dict[str, Any]:
        served_processes, unserved_processes, app_component_services = self._analyze_processes()
        application_usage = self._analyze_application_usage()  # Add new analysis method
        
        return {
            'served_processes': served_processes,
            'unserved_processes': unserved_processes,
            'app_component_services': app_component_services,
            'application_usage': application_usage  # Add new data to results
        }
    
    def _analyze_application_usage(self):
        # Your new analysis logic here
        pass
```

## Best Practices

### 1. Data Processing
- Keep data processing logic in the report class
- Break down complex processing into smaller, well-named methods
- Use type hints for better code readability and IDE support
- Document your methods with docstrings

### 2. Report Structure
- Follow the existing pattern of separating data processing from formatting
- Use meaningful method names that describe what they do
- Keep the `generate` method clean and high-level
- Handle errors gracefully

### 3. Code Organization
```python
class YourNewReport(BaseReport):
    def generate(self, data):
        # High-level flow
        processed_data = self._process_data(data)
        formatted_data = self._format_data(processed_data)
        self._export_data(formatted_data)
    
    def _process_data(self, data):
        # Data processing logic
        pass
    
    def _format_data(self, processed_data):
        # Data formatting logic
        pass
    
    def _export_data(self, formatted_data):
        # Export using the exporter
        pass
```

## Testing Your New Report

1. Create test data:
```python
# tests/test_your_report.py
def test_your_report():
    test_data = {
        'key': 'value'
        # Add test data matching your report's needs
    }
    
    exporter = MockExporter()
    report = YourNewReport(exporter)
    report.generate(test_data)
    
    # Assert expected results
```

2. Run your report:
```bash
python main.py --report <your_report_number> --file data/kg-tax.xml
```

## Common Pitfalls to Avoid

1. **Data Validation**: Always validate input data before processing
2. **Error Handling**: Include appropriate error messages for missing or invalid data
3. **Memory Usage**: Be mindful of memory usage when processing large datasets
4. **Code Duplication**: Reuse existing functionality when possible
5. **Documentation**: Always update the help text in `main.py` with your new report option

## Example Report Implementation

Here's a complete example of a new report that analyzes application dependencies:

```python
from typing import Dict, Any, List
from .base import BaseReport

class ApplicationDependencyReport(BaseReport):
    """Report generator for application dependencies"""
    
    def generate(self, data: Dict[str, Any]) -> None:
        dependencies = self._analyze_dependencies(data)
        formatted_data = self._format_dependencies(dependencies)
        
        self.exporter.export_data(
            header="Application Dependencies Analysis",
            data=formatted_data,
            columns=['Application', 'Depends On', 'Dependency Type']
        )
    
    def _analyze_dependencies(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        dependencies = []
        # Analysis logic here
        return dependencies
    
    def _format_dependencies(self, dependencies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # Formatting logic here
        return sorted(dependencies, key=lambda x: x['Application'])
```

## Need Help?

If you encounter any issues while adding a new report:
1. Check existing report implementations for patterns and examples
2. Review the base classes (`BaseReport`, `BaseAnalyzer`, `BaseExporter`)
3. Ensure all required data is available in the analyzer results
4. Test your report with both console and CSV exporters

