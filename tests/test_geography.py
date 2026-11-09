import pandas as pd

from src.analysis import geography


def test_analyse_severity_by_district_calls_stacked_bar_chart(mocker):
    """Ensure severity data is transformed and charted."""

    mock_chart = mocker.patch(
        "src.analysis.geography.stacked_bar_chart"
    )

    df = pd.DataFrame(
        {
            "local_authority_ons_district": [
                "E08000035",  # Leeds
                "E08000032",  # Bradford
                "E08000035",
            ],
            "collision_severity": [
                1, 2, 3,
            ],
        }
    )

    geography.analyse_severity_by_district(df)

    mock_chart.assert_called_once()

    args = mock_chart.call_args[0]

    assert args[1] == "Accident Severity Breakdown by West Yorkshire District"
    assert args[2] == "District"
    assert args[3] == "Number of Accidents"


def test_run_geographical_suite_calls_analysis(mocker):
    """Ensure the geographical suite executes the analysis function."""

    mock_analysis = mocker.patch(
        "src.analysis.geography.analyse_severity_by_district"
    )

    geography.run_geographical_suite(pd.DataFrame())

    mock_analysis.assert_called_once()