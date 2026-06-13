import pandas as pd
from unittest.mock import patch
from src.analysis.summary_analysis import run_comprehensive_summary


def test_run_comprehensive_summary_basic():

    df = pd.DataFrame(
        {
            "first_road_class": [1, 2, 2],
            "weather_conditions": [1, 1, 2],
            "light_conditions": [3, 3, 3],
            "collision_severity": [1, 2, 3],
        }
    )

    vehicles_df = pd.DataFrame(
        {"sex_of_driver": [1, 1, 2], "generic_make_model": ["Ford", "Golf", "BMW"]}
    )

    with (
        patch("src.analysis.summary_analysis.pie_chart") as mock_chart,
        patch(
            "src.analysis.summary_analysis.severity_labels",
            {1: "Fatal", 2: "Serious", 3: "Slight"},
        ),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine", 2: "Rain"}),
        patch("src.analysis.summary_analysis.light_labels", {3: "Darkness"}),
        patch("src.analysis.summary_analysis.gender_options", {1: "Male", 2: "Female"}),
    ):
        result = run_comprehensive_summary(df, vehicles_df)

        # Validate key lines
        assert "TOTAL DATASET: 3 records analyzed." in result[0]
        assert "MOTORWAY SCOPE: 1 incidents (33.3% of total)." in result[1]
        assert "Primary Driver Gender: Male" in result[4]
        assert "Most Frequent Vehicle: BMW" in result[5]
        assert "Predominant Weather: Fine" in result[8]
        assert "Predominant Lighting: Darkness" in result[9]
        assert " - Fatal: 1" in result[12]
        assert " - Serious: 1" in result[13]
        assert " - Slight: 1" in result[14]
        assert "REGIONAL HAZARD SCORE: 66.7%" in result[-1]

        # Validate pie chart call
        mock_chart.assert_called_once()


def test_run_comprehensive_summary_empty_vehicles():

    df = pd.DataFrame(
        {
            "first_road_class": [1],
            "weather_conditions": [1],
            "light_conditions": [1],
            "collision_severity": [1],
        }
    )

    vehicles_df = pd.DataFrame()

    with (
        patch("src.analysis.summary_analysis.pie_chart"),
        patch("src.analysis.summary_analysis.severity_labels", {1: "Fatal"}),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine"}),
        patch("src.analysis.summary_analysis.light_labels", {1: "Daylight"}),
    ):
        result = run_comprehensive_summary(df, vehicles_df)

        assert "Primary Driver Gender: Unknown" in result[4]
        assert "Most Frequent Vehicle: Unknown" in result[5]


def test_vehicle_make_filtering():
    df = pd.DataFrame(
        {
            "first_road_class": [2],
            "weather_conditions": [1],
            "light_conditions": [1],
            "collision_severity": [1],
        }
    )

    vehicles_df = pd.DataFrame(
        {"sex_of_driver": [1, 1], "generic_make_model": ["-1", "Toyota"]}
    )

    with (
        patch("src.analysis.summary_analysis.pie_chart"),
        patch("src.analysis.summary_analysis.severity_labels", {1: "Fatal"}),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine"}),
        patch("src.analysis.summary_analysis.light_labels", {1: "Daylight"}),
        patch("src.analysis.summary_analysis.gender_options", {1: "Male"}),
    ):
        result = run_comprehensive_summary(df, vehicles_df)

        assert "Most Frequent Vehicle: Toyota" in result[5]


def test_severity_mapping_and_hazard_score():
    df = pd.DataFrame(
        {
            "first_road_class": [2, 2, 2],
            "weather_conditions": [1, 1, 1],
            "light_conditions": [1, 1, 1],
            "collision_severity": [1, 1, 3],  # 2 Fatal, 1 Slight
        }
    )

    vehicles_df = pd.DataFrame()

    with (
        patch("src.analysis.summary_analysis.pie_chart"),
        patch(
            "src.analysis.summary_analysis.severity_labels", {1: "Fatal", 3: "Slight"}
        ),
        patch("src.analysis.summary_analysis.weather_labels", {1: "Fine"}),
        patch("src.analysis.summary_analysis.light_labels", {1: "Daylight"}),
    ):
        result = run_comprehensive_summary(df, vehicles_df)

        assert " - Fatal: 2" in result
        assert " - Slight: 1" in result
        assert "REGIONAL HAZARD SCORE: 66.7%" in result[-1]
