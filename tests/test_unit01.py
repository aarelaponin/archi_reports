import pytest
from io import StringIO
import sys
from contextlib import contextmanager

from archi_reports.analyzers.archimate import ArchimateAnalyzer
from archi_reports.reports.process_status import ProcessStatusReport
from archi_reports.reports.component_services import ComponentServicesReport
from archi_reports.exporters.console import ConsoleExporter

# Sample XML for testing
SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<model xmlns="http://www.opengroup.org/xsd/archimate/3.0/"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <elements>
        <element identifier="BP1" xsi:type="BusinessProcess">
            <name>Order Processing</name>
        </element>
        <element identifier="BP2" xsi:type="BusinessProcess">
            <name>Invoice Generation</name>
        </element>
        <element identifier="BP3" xsi:type="BusinessProcess">
            <name>Manual Review</name>
        </element>
        <element identifier="AC1" xsi:type="ApplicationComponent">
            <name>Order System</name>
        </element>
        <element identifier="AC2" xsi:type="ApplicationComponent">
            <name>Billing System</name>
        </element>
    </elements>
    <relationships>
        <relationship identifier="REL1" source="AC1" target="BP1" xsi:type="Serving"/>
        <relationship identifier="REL2" source="AC2" target="BP2" xsi:type="Serving"/>
    </relationships>
</model>
"""


@contextmanager
def captured_output():
    """Context manager to capture stdout"""
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


@pytest.fixture
def analyzer():
    """Fixture providing configured analyzer"""
    return ArchimateAnalyzer(SAMPLE_XML)


@pytest.fixture
def analysis_results(analyzer):
    """Fixture providing analysis results"""
    return analyzer.analyze()


def test_process_count(analysis_results):
    """Test that all processes are found"""
    total_processes = (
            len(analysis_results['served_processes']) +
            len(analysis_results['unserved_processes'])
    )
    assert total_processes == 3


def test_served_processes(analysis_results):
    """Test identification of served processes"""
    served_names = {p.name for p in analysis_results['served_processes']}
    assert served_names == {'Order Processing', 'Invoice Generation'}


def test_unserved_processes(analysis_results):
    """Test identification of unserved processes"""
    unserved_names = {p.name for p in analysis_results['unserved_processes']}
    assert unserved_names == {'Manual Review'}


def test_component_services(analysis_results):
    """Test mapping of components to processes"""
    expected_mapping = {
        'Order System': ['Order Processing'],
        'Billing System': ['Invoice Generation']
    }
    assert analysis_results['app_component_services'] == expected_mapping


def test_process_status_report_served(analysis_results):
    """Test process status report for served processes"""
    exporter = ConsoleExporter()
    report = ProcessStatusReport(exporter, show_served=True)

    with captured_output() as output:
        report.generate(analysis_results)

    output_text = output.getvalue()
    # Test report header
    assert 'Process Status Report: Served Business Processes' in output_text

    # Test process entries
    assert 'Order Processing - Order System' in output_text
    assert 'Invoice Generation - Billing System' in output_text

    # Test count
    assert 'Found 2 items:' in output_text


def test_process_status_report_unserved(analysis_results):
    """Test process status report for unserved processes"""
    exporter = ConsoleExporter()
    report = ProcessStatusReport(exporter, show_served=False)

    with captured_output() as output:
        report.generate(analysis_results)

    output_text = output.getvalue()
    assert 'Manual Review' in output_text
    assert 'Order Processing' not in output_text


def test_component_services_report(analysis_results):
    """Test component services report"""
    exporter = ConsoleExporter()
    report = ComponentServicesReport(exporter)

    with captured_output() as output:
        report.generate(analysis_results)

    output_text = output.getvalue()
    assert 'Order System' in output_text
    assert 'Billing System' in output_text
    assert 'Order Processing' in output_text
    assert 'Invoice Generation' in output_text