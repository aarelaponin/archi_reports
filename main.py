#!/usr/bin/env python3
import argparse
from src.archi_reports.analyzers.archimate import ArchimateAnalyzer
from src.archi_reports.reports.process_status import ProcessStatusReport
from src.archi_reports.reports.component_services import ComponentServicesReport
from src.archi_reports.exporters.console import ConsoleExporter
from src.archi_reports.exporters.csv import CsvExporter


def main():
    parser = argparse.ArgumentParser(
        description='Analyze business processes in Archimate model',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--report',
        type=int,
        choices=[1, 2],
        default=1,
        help='Report type: 1=Processes by served/unserved status, 2=Application Components with their served processes'
    )
    parser.add_argument(
        '--file',
        default='data/kg-tax.xml',
        help='Path to the XML file'
    )
    parser.add_argument(
        '--served',
        action='store_true',
        help='Show served processes instead of unserved ones (only for report type 1)'
    )
    parser.add_argument(
        '--format',
        choices=['console', 'csv'],
        default='console',
        help='Output format for the report'
    )

    args = parser.parse_args()

    try:
        # Read and analyze the XML file
        with open(args.file, 'r', encoding='utf-8') as file:
            analyzer = ArchimateAnalyzer(file.read())

        # Get analysis results
        analysis_results = analyzer.analyze()

        # Create appropriate exporter
        exporter = (CsvExporter(f"report_{args.report}")
                    if args.format == 'csv'
                    else ConsoleExporter())

        # Generate the requested report
        if args.report == 1:
            report_generator = ProcessStatusReport(exporter, show_served=args.served)
        else:
            report_generator = ComponentServicesReport(exporter)

        report_generator.generate(analysis_results)

    except Exception as e:
        print(f"Error processing the file: {str(e)}")
        raise


if __name__ == "__main__":
    main()
