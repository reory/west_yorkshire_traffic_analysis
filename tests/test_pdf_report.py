import pytest
import os
import shutil
import base64
from src.analysis.report_generator import generate_pdf_report

def test_generate_pdf_report_flow(tmp_path):
    """Verifies the PDF is created and handles missing assets."""

    # Set up Mock Folders
    chart_dir = tmp_path / 'output_charts'
    chart_dir.mkdir()

    # Create a dummy assets folder so the logo call dosen't crash.
    assets_dir = tmp_path / 'assets'
    assets_dir.mkdir()

    # Create a fake logo (using pixels) so fpdf does not crash.
    pixel_png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')
    logo_file = assets_dir / 'logo.png'
    logo_file.write_bytes(pixel_png)

    # Set up mock data.
    summary = ['Total Accidents: 10', 'Most Dangerous Day: Friday']

    hotspots = [{
        'latitude': 53.8,
        'longitude': -1.5,
        'site_label': "Test Site",
        'road_type': 'A-Road',
        'count': 5
    }]

    # Run Generator
    try:
        os.chdir(tmp_path)
        generate_pdf_report(summary, hotspots, chart_folder=str(chart_dir))

    except FileNotFoundError as e:
        pytest.fail(f'PDF Generator crashed!: {e}')

    # Assertions
    expected_pdf = chart_dir / "West_Yorkshire_Traffic_Analysis_Report.pdf"
    assert expected_pdf.exists()
    assert expected_pdf.stat().st_size > 0