# Developer Manual: Adding New Exporters to Archimate Analyzer

## Overview
This manual explains how to add new export formats to the Archimate Analyzer system. The exporter system is designed to be modular, allowing developers to add new export formats (like JSON, Excel, HTML, etc.) without modifying existing code.

## Step-by-Step Guide

### 1. Create a New Exporter Class
First, create a new Python file in the `src/archi_reports/exporters/` directory. Name it according to your export format (e.g., `json_exporter.py` for JSON export).

```python
# src/archi_reports/exporters/json_exporter.py
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from .base import BaseExporter

class JsonExporter(BaseExporter):
    """Exporter for JSON format"""
    
    def __init__(self, report_type: str):
        self.report_type = report_type
    
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        """
        Export data in JSON format
        
        Args:
            header: Report header/title
            data: List of dictionaries containing the data
            columns: List of column names
        """
        os.makedirs('reports', exist_ok=True)
        filename = f"reports/{self.report_type}_{datetime.now():%Y%m%d_%H%M%S}.json"
        
        # Prepare the output structure
        output = {
            "header": header,
            "columns": columns,
            "data": data,
            "generated_at": datetime.now().isoformat()
        }
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
```

### 2. Update the Main Script
Modify `main.py` to include your new export format:

```python
# Add import
from src.archi_reports.exporters.json_exporter import JsonExporter

# Update argument parser
parser.add_argument(
    '--format',
    choices=['console', 'csv', 'json'],  # Add your new format
    default='console',
    help='Output format for the report'
)

# Update exporter selection
def get_exporter(format_type: str, report_num: int) -> BaseExporter:
    if format_type == 'csv':
        return CsvExporter(f"report_{report_num}")
    elif format_type == 'json':
        return JsonExporter(f"report_{report_num}")
    else:
        return ConsoleExporter()

# In main():
exporter = get_exporter(args.format, args.report)
```

## Best Practices

### 1. File Handling
```python
class YourExporter(BaseExporter):
    def __init__(self, report_type: str):
        self.report_type = report_type
        self.output_dir = 'reports'
    
    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _get_filename(self) -> str:
        """Generate unique filename"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{self.output_dir}/{self.report_type}_{timestamp}.{self.extension}"
    
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        self._ensure_output_dir()
        filename = self._get_filename()
        self._write_data(filename, header, data, columns)
```

### 2. Error Handling
Always include proper error handling in your exporter:

```python
class ExcelExporter(BaseExporter):
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        try:
            self._ensure_output_dir()
            filename = self._get_filename()
            
            # Your export logic here
            
        except PermissionError:
            raise Exception(f"Permission denied when writing to {filename}")
        except Exception as e:
            raise Exception(f"Error exporting data: {str(e)}")
```

### 3. Data Validation
Validate input data before processing:

```python
class BaseExporter(ABC):
    def _validate_data(self, data: List[Dict[str, Any]], columns: List[str]) -> None:
        """Validate input data"""
        if not isinstance(data, list):
            raise ValueError("Data must be a list of dictionaries")
        
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("Each data item must be a dictionary")
        
        if not all(col in item for item in data for col in columns):
            raise ValueError("All columns must exist in each data item")
```

## Example Implementations

### 1. Excel Exporter
```python
# src/archi_reports/exporters/excel_exporter.py
from openpyxl import Workbook
from typing import List, Dict, Any
from .base import BaseExporter

class ExcelExporter(BaseExporter):
    def __init__(self, report_type: str):
        self.report_type = report_type
        self.extension = 'xlsx'
    
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        wb = Workbook()
        ws = wb.active
        ws.title = "Report"
        
        # Write header
        ws['A1'] = header
        
        # Write column headers
        for col_idx, column in enumerate(columns, 1):
            ws.cell(row=2, column=col_idx, value=column)
        
        # Write data
        for row_idx, item in enumerate(data, 3):
            for col_idx, column in enumerate(columns, 1):
                ws.cell(row=row_idx, column=col_idx, value=item[column])
        
        # Save workbook
        filename = self._get_filename()
        wb.save(filename)
```

### 2. HTML Exporter
```python
# src/archi_reports/exporters/html_exporter.py
from typing import List, Dict, Any
from .base import BaseExporter

class HtmlExporter(BaseExporter):
    def __init__(self, report_type: str):
        self.report_type = report_type
        self.extension = 'html'
    
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        html_content = ['<!DOCTYPE html>', '<html>', '<body>']
        html_content.append(f'<h1>{header}</h1>')
        
        # Create table
        html_content.append('<table border="1">')
        
        # Add header row
        html_content.append('<tr>')
        for column in columns:
            html_content.append(f'<th>{column}</th>')
        html_content.append('</tr>')
        
        # Add data rows
        for item in data:
            html_content.append('<tr>')
            for column in columns:
                html_content.append(f'<td>{item[column]}</td>')
            html_content.append('</tr>')
        
        html_content.extend(['</table>', '</body>', '</html>'])
        
        # Write to file
        filename = self._get_filename()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_content))
```

## Testing Your New Exporter

1. Create unit tests:
```python
# tests/test_exporters.py
import pytest
from src.archi_reports.exporters.your_exporter import YourExporter

def test_your_exporter():
    exporter = YourExporter("test_report")
    test_data = [
        {"col1": "val1", "col2": "val2"},
        {"col1": "val3", "col2": "val4"}
    ]
    columns = ["col1", "col2"]
    
    exporter.export_data("Test Header", test_data, columns)
    
    # Add assertions to verify the output
```

2. Test with actual reports:
```bash
python main.py --report 1 --format your_format
```

## Common Pitfalls to Avoid

1. **File Permissions**: Always handle permission-related errors
2. **Character Encoding**: Use proper encoding (usually UTF-8)
3. **Memory Usage**: Consider streaming for large datasets
4. **File Extensions**: Use appropriate file extensions
5. **Dependencies**: Document any required third-party libraries

## Need Help?

If you encounter issues while adding a new exporter:
1. Review existing exporter implementations
2. Check the `BaseExporter` class for required methods
3. Ensure proper error handling
4. Test with various data types and sizes
5. Verify file permissions in the output directory

