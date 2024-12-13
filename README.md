# Archimate Analyzer

A Python-based tool for analyzing Archimate XML models and generating various reports about business processes, application components, and their relationships.

## Features

- Parse and analyze Archimate XML models
- Generate multiple report types:
  - Process Status Report (served/unserved processes)
  - Component Services Report (application components and their processes)
- Support multiple output formats:
  - Console output
  - CSV export

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/archimate-analyzer.git
cd archimate-analyzer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The basic command structure is:
```bash
python main.py --report <report_type> --file <input_file> [options]
```

### Command Line Options

- `--report`: Report type to generate (required)
  - `1`: Process Status Report
  - `2`: Component Services Report
- `--file`: Path to the input XML file (default: 'data/kg-tax.xml')
- `--served`: Show served processes instead of unserved ones (only for report type 1)
- `--format`: Output format ('console' or 'csv', default: 'console')

### Examples

1. Generate a report of unserved processes:
```bash
python main.py --report 1 --file data/kg-tax.xml
```

2. Generate a report of served processes in CSV format:
```bash
python main.py --report 1 --served --format csv
```

3. Generate a component services report:
```bash
python main.py --report 2
```

## Project Structure

```
archimate-analyzer/
├── data/                    # Input data files
│   └── kg-tax.xml
├── reports/                 # Generated reports (CSV)
├── src/
│   └── archi_reports/
│       ├── analyzers/      # Model analysis logic
│       ├── exporters/      # Output format handlers
│       ├── models/         # Data models
│       └── reports/        # Report generators
├── tests/                  # Test files
├── main.py                 # Main entry point
├── README.md
└── requirements.txt
```

## Extending the Tool

### Adding New Reports

1. Create a new report class in `src/archi_reports/reports/`
2. Inherit from `BaseReport`
3. Implement the `generate` method
4. Update `main.py` to include the new report option

Example:
```python
# src/archi_reports/reports/your_report.py
from typing import Dict, Any
from .base import BaseReport

class YourReport(BaseReport):
    def generate(self, data: Dict[str, Any]) -> None:
        # Your report generation logic here
        formatted_data = self._format_data(data)
        self.exporter.export_data(
            header="Your Report Title",
            data=formatted_data,
            columns=['Column1', 'Column2']
        )
```

### Adding New Export Formats

1. Create a new exporter class in `src/archi_reports/exporters/`
2. Inherit from `BaseExporter`
3. Implement the `export_data` method
4. Update `main.py` to include the new format option

Example:
```python
# src/archi_reports/exporters/your_exporter.py
from typing import List, Dict, Any
from .base import BaseExporter

class YourExporter(BaseExporter):
    def export_data(self, header: str, data: List[Dict[str, Any]], columns: List[str]) -> None:
        # Your export logic here
        pass
```

## Development

### Setting Up Development Environment

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. To check your code:
```bash
flake8 src/ tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Aare Laponin - Initial work - [YourGitHub](https://github.com/aarelaponin)

## Acknowledgments

- The Open Group for Archimate specifications
- Contributors and maintainers of the project

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**:
   - Ensure you're in the project root directory
   - Verify virtual environment is activated
   - Check if all dependencies are installed

2. **XML Parsing Errors**:
   - Verify the input XML file is valid Archimate format
   - Check file encoding (should be UTF-8)

3. **Permission Errors**:
   - Ensure write permissions in the reports directory
   - Check if output files are not locked by other applications

### Getting Help

If you encounter issues:
1. Check the existing issues on GitHub
2. Review the documentation
3. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Expected vs actual behavior

## Future Plans

- Support for additional Archimate model versions
- More report types (dependencies, impact analysis)
- Additional export formats (Excel, PDF)
- Interactive web interface
- Batch processing of multiple models

