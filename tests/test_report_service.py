import pandas as pd

from src.analysis.report_service import build_report


def test_build_report_returns_pdf_path(mocker, tmp_path):
    """Report service should return the generated PDF path."""

    mocker.patch(
        "src.analysis.report_service.identify_blackspots",
        return_value=[],
    )

    mocker.patch(
        "src.analysis.report_service.generate_blackspots_chart",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_weather_distribution",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_light_conditions",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_road_surface",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_special_conditions",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_severity_by_district",
    )

    mocker.patch(
        "src.analysis.report_service.run_comprehensive_summary",
        return_value=["Test Summary"],
    )

    mock_pdf = mocker.patch(
        "src.analysis.report_service.generate_pdf_report",
        return_value="temp_report/test.pdf",
    )

    accidents_df = pd.DataFrame(
        {
            "collision_index": ["A1"],
            "latitude": [53.8],
            "longitude": [-1.5],
        }
    )

    vehicles_df = pd.DataFrame()

    casualties_df = pd.DataFrame(
        {
            "sex_of_casualty": [1, 2],
            "collision_index": [1, 2],
        }
    )

    result = build_report(
        accidents_df,
        vehicles_df,
        casualties_df,
        data_duration="2024",
        chart_folder=str(tmp_path)
    )

    assert result == "temp_report/test.pdf"

    mock_pdf.assert_called_once()


def test_build_report_passes_chart_folder(mocker, tmp_path):
    """Chart folder should be passed through to PDF generation."""

    mocker.patch(
        "src.analysis.report_service.identify_blackspots",
        return_value=[],
    )

    mocker.patch(
        "src.analysis.report_service.generate_blackspots_chart",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_weather_distribution",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_light_conditions",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_road_surface",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_special_conditions",
    )

    mocker.patch(
        "src.analysis.report_service.analyse_severity_by_district",
    )

    mocker.patch(
        "src.analysis.report_service.run_comprehensive_summary",
        return_value=["Test Summary"],
    )

    mock_pdf = mocker.patch(
        "src.analysis.report_service.generate_pdf_report",
        return_value="test.pdf",
    )

    build_report(
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        chart_folder="temp_report",
    )

    _, kwargs = mock_pdf.call_args

    assert kwargs["chart_folder"] == "temp_report"