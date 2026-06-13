import pandas as pd
from unittest.mock import patch
from src.analysis.infrastructure import (
    analyse_road_type_distribution,
    analyse_urban_rural_proportion,
    analyse_speed_limit_distribution,
    run_infrastructure_suite,
)


def test_analyse_road_type_distribution():
    df = pd.DataFrame({"display_road_type": ["A Road", "A Road", "Motorway"]})

    with patch("src.analysis.infrastructure.bar_chart") as mock_bar:
        analyse_road_type_distribution(df)

        expected = df["display_road_type"].value_counts()

        args, kwargs = mock_bar.call_args

        assert args[0].equals(expected)
        assert args[1] == "Collisions by Road Type (West Yorkshire)"
        assert args[2] == "Road Type"
        assert args[3] == "Number of Collisions"
        assert kwargs["color"] == "#56CF5AFF"


def test_analyse_urban_rural_proportion():
    df = pd.DataFrame({"urban_or_rural_area": [1, 2, 1]})

    with (
        patch("src.analysis.infrastructure.pie_chart") as mock_pie,
        patch(
            "src.analysis.infrastructure.urban_rural_labels", {1: "Urban", 2: "Rural"}
        ),
    ):
        analyse_urban_rural_proportion(df)

        df_local = df.copy()
        df_local["area_label"] = df_local["urban_or_rural_area"].map(
            {1: "Urban", 2: "Rural"}
        )
        expected = df_local["area_label"].value_counts()

        args, kwargs = mock_pie.call_args

        assert args[0].equals(expected)
        assert args[1] == "Proportion of Urban vs Rural Collisions (West Yorkshire)"
        assert kwargs["pctdistance"] == 0.8
        assert kwargs["labeldistance"] == 1.0
        assert kwargs["colors"] == ["#8cb49d", "#fd0707"]


def test_analyse_speed_limit_distribution():
    df = pd.DataFrame({"speed_limit": [30, 20, 30, 40]})

    with patch("src.analysis.infrastructure.bar_chart") as mock_bar:
        analyse_speed_limit_distribution(df)

        expected = df["speed_limit"].value_counts().sort_index()

        args, kwargs = mock_bar.call_args

        assert args[0].equals(expected)
        assert args[1] == "Collisions by Speed Limit (West Yorkshire)"
        assert args[2] == "Speed Limit (mph)"
        assert args[3] == "Number of Collisions"
        assert kwargs["color"] == "#3cbaf0ff"


def test_run_infrastructure_suite():
    df = pd.DataFrame(
        {
            "display_road_type": ["A Road"],
            "urban_or_rural_area": [1],
            "speed_limit": [30],
        }
    )

    with (
        patch("src.analysis.infrastructure.analyse_road_type_distribution") as r,
        patch("src.analysis.infrastructure.analyse_speed_limit_distribution") as s,
        patch("src.analysis.infrastructure.analyse_urban_rural_proportion") as u,
    ):
        run_infrastructure_suite(df)

        r.assert_called_once_with(df)
        s.assert_called_once_with(df)
        u.assert_called_once_with(df)
