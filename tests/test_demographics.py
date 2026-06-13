import pandas as pd
from unittest.mock import patch
from src.analysis.demographics import run_demographic_suite


def test_driver_gender_distribution():
    vehicles_df = pd.DataFrame({"sex_of_driver": [1, 1, 2]})
    casualties_df = pd.DataFrame()

    with (
        patch("src.analysis.demographics.pie_chart") as mock_pie,
        patch("src.analysis.demographics.gender_options", {1: "Male", 2: "Female"}),
    ):
        run_demographic_suite(vehicles_df, casualties_df)

        expected = (
            vehicles_df["sex_of_driver"].map({1: "Male", 2: "Female"}).value_counts()
        )

        args, kwargs = mock_pie.call_args

        assert args[0].equals(expected)
        assert args[1] == "Driver Gender Distribution West Yorkshire"
        assert kwargs["pctdistance"] == 1.0
        assert kwargs["labeldistance"] == 0.5


def test_driver_age_band_distribution():
    vehicles_df = pd.DataFrame(
        {
            "age_band_of_driver": [1, 2, -1]  # -1 should be filtered out
        }
    )
    casualties_df = pd.DataFrame()

    with (
        patch("src.analysis.demographics.bar_chart") as mock_bar,
        patch("src.analysis.demographics.age_band_labels", {1: "17-25", 2: "26-35"}),
    ):
        run_demographic_suite(vehicles_df, casualties_df)

        valid = vehicles_df[vehicles_df["age_band_of_driver"] != -1].copy()
        valid["age_range"] = valid["age_band_of_driver"].map({1: "17-25", 2: "26-35"})
        expected = (
            valid["age_range"].value_counts().reindex(["17-25", "26-35"]).dropna()
        )

        args, kwargs = mock_bar.call_args

        assert args[0].equals(expected)
        assert args[1] == "Collisions By Driver Age Band"
        assert args[2] == "Age Group"
        assert args[3] == "Count"
        assert kwargs["color"] == "#0698FA"


def test_casualty_class_distribution():
    vehicles_df = pd.DataFrame()
    casualties_df = pd.DataFrame({"casualty_class": [1, 2, 1]})

    with (
        patch("src.analysis.demographics.bar_chart") as mock_bar,
        patch(
            "src.analysis.demographics.casualty_class_labels",
            {1: "Driver", 2: "Passenger"},
        ),
    ):
        run_demographic_suite(vehicles_df, casualties_df)

        expected = (
            casualties_df["casualty_class"]
            .map({1: "Driver", 2: "Passenger"})
            .value_counts()
        )

        args, kwargs = mock_bar.call_args

        assert args[0].equals(expected)
        assert args[1] == "Casualty Type Distribution"
        assert args[2] == "Type of Person"
        assert args[3] == "Count"
        assert kwargs["color"] == "#5d88f4"


def test_top_vehicle_makes():
    vehicles_df = pd.DataFrame(
        {"generic_make_model": ["Ford", "-1", "BMW", "Ford", -1]}
    )
    casualties_df = pd.DataFrame()

    with patch("src.analysis.demographics.bar_chart") as mock_bar:
        run_demographic_suite(vehicles_df, casualties_df)

        valid = vehicles_df[
            (vehicles_df["generic_make_model"] != "-1")
            & (vehicles_df["generic_make_model"] != -1)
        ]
        expected = valid["generic_make_model"].value_counts().head(10)

        args, kwargs = mock_bar.call_args

        assert args[0].equals(expected)
        assert args[1] == "Top 10 Vehicle Makes in West Yorkshire Collisions"
        assert args[2] == "Vehicle Make/Model"
        assert args[3] == "Total Incidents"
        assert kwargs["color"] == "#667294"
