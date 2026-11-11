from unittest.mock import patch

import pandas as pd

from src.analysis.summary_analysis import run_comprehensive_summary


def test_run_comprehensive_summary_basic():
    """Tests comprehensive summary output."""

    df = pd.DataFrame(
        {
            "first_road_class": [1, 2, 2],
            "weather_conditions": [1, 1, 2],
            "light_conditions": [3, 3, 3],
            "collision_severity": [1, 2, 3],
        }
    )

    vehicles_df = pd.DataFrame(
        {
            "sex_of_driver": [1, 1, 2],
            "generic_make_model": ["Ford", "Golf", "BMW"],
        }
    )

    casualties_df = pd.DataFrame(
        {
            "sex_of_casualty": [2, 2, 1],
        }
    )

    with (
        patch("src.analysis.summary_analysis.pie_chart") as mock_chart,
        patch(
            "src.analysis.summary_analysis.severity_labels",
            {1: "Fatal", 2: "Serious", 3: "Slight"},
        ),
        patch(
            "src.analysis.summary_analysis.weather_labels",
            {1: "Fine", 2: "Rain"},
        ),
        patch(
            "src.analysis.summary_analysis.light_labels",
            {3: "Darkness"},
        ),
        patch(
            "src.analysis.summary_analysis.gender_options",
            {1: "Male", 2: "Female"},
        ),
    ):
        result = run_comprehensive_summary(
            df,
            vehicles_df,
            casualties_df,
        )

        assert "TOTAL DATASET: 3 records analysed." in result
        assert "MOTORWAY INCIDENTS: 1 incidents (33.3% of total)." in result

        assert any(
            "Predominant Casualty Gender: Female" in line
            for line in result
        )

        assert any(
            "Most Common Vehicle Model: BMW" in line
            for line in result
        )

        assert any(
            "Predominant Weather: Fine" in line
            for line in result
        )

        assert any(
            "Predominant Lighting: Darkness" in line
            for line in result
        )

        assert " - Fatal: 1" in result
        assert " - Serious: 1" in result
        assert " - Slight: 1" in result

        assert any(
            "REGIONAL HAZARD SCORE: 66.7%" in line
            for line in result
        )

        mock_chart.assert_called_once()


def test_run_comprehensive_summary_empty_vehicles():
    """Tests summary with missing vehicles."""

    df = pd.DataFrame(
        {
            "first_road_class": [1],
            "weather_conditions": [1],
            "light_conditions": [1],
            "collision_severity": [1],
        }
    )

    vehicles_df = pd.DataFrame()

    casualties_df = pd.DataFrame(
        {
            "sex_of_casualty": [2, 2, 1],
        }
    )

    with (
        patch("src.analysis.summary_analysis.pie_chart"),
        patch("src.analysis.summary_analysis.severity_labels", {1: "Fatal"}),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine"}),
        patch("src.analysis.summary_analysis.light_labels", {1: "Daylight"}),
        patch(
            "src.analysis.summary_analysis.gender_options",
            {1: "Male", 2: "Female"},
        ),
    ):
        result = run_comprehensive_summary(
            df,
            vehicles_df,
            casualties_df,
        )

        assert any(
            "Predominant Casualty Gender: Female" in line
            for line in result
        )

        assert any(
            "Most Common Vehicle Model: Unknown" in line
            for line in result
        )


def test_vehicle_make_filtering():
    """Tests vehicle make filtering."""

    df = pd.DataFrame(
        {
            "first_road_class": [2],
            "weather_conditions": [1],
            "light_conditions": [1],
            "collision_severity": [1],
        }
    )

    vehicles_df = pd.DataFrame(
        {
            "sex_of_driver": [1, 1],
            "generic_make_model": ["-1", "Toyota"],
        }
    )

    casualties_df = pd.DataFrame(
        {
            "sex_of_casualty": [2, 2, 1],
        }
    )

    with (
        patch("src.analysis.summary_analysis.pie_chart"),
        patch("src.analysis.summary_analysis.severity_labels", {1: "Fatal"}),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine"}),
        patch("src.analysis.summary_analysis.light_labels", {1: "Daylight"}),
        patch(
            "src.analysis.summary_analysis.gender_options",
            {1: "Male", 2: "Female"},
        ),
    ):
        result = run_comprehensive_summary(
            df,
            vehicles_df,
            casualties_df,
        )

        assert any("Most Common Vehicle Model: Toyota" in line for line in result)


def test_severity_mapping_and_hazard_score():
    """Tests severity mapping and scoring."""

    df = pd.DataFrame(
        {
            "first_road_class": [2, 2, 2],
            "weather_conditions": [1, 1, 1],
            "light_conditions": [1, 1, 1],
            "collision_severity": [1, 1, 3],
        }
    )

    vehicles_df = pd.DataFrame()

    casualties_df = pd.DataFrame(
        {
            "sex_of_casualty": [2, 2, 1],
        }
    )

    with (
        patch("src.analysis.summary_analysis.pie_chart"),
        patch(
            "src.analysis.summary_analysis.severity_labels",
            {1: "Fatal", 3: "Slight"},
        ),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine"}),
        patch("src.analysis.summary_analysis.light_labels", {1: "Daylight"}),
    ):
        result = run_comprehensive_summary(df, vehicles_df, casualties_df)

        assert " - Fatal: 2" in result
        assert " - Slight: 1" in result
        assert any("REGIONAL HAZARD SCORE: 66.7%" in line for line in result
        )