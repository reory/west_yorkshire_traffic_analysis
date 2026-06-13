import pandas as pd
from unittest.mock import patch
from src.analysis.temporal import (
    analyse_hour_distribution,
    analyse_weekday_distribution,
    analyse_month_distribution,
    run_temporal_suite,
)


def test_analyse_hour_distribution_calls_bar_chart():

    df = pd.DataFrame({"hour": [1, 1, 2]})

    with patch("src.analysis.temporal.bar_chart") as mock_chart:
        analyse_hour_distribution(df)

        # Hour counts should be {1:2, 2:1}
        expected = df["hour"].value_counts().sort_index()

        mock_chart.assert_called_once()
        args, kwargs = mock_chart.call_args

        assert args[0].equals(expected)
        assert args[1] == "Collisions by Hour of Day (West Yorkshire)"
        assert args[2] == "Hour(24h)"
        assert args[3] == "Number of Collisions"
        assert kwargs["color"] == "steelblue"


def test_analyse_weekday_distribution_calls_bar_chart():
    df = pd.DataFrame({"day_name": ["Monday", "Wednesday", "Monday"]})

    with patch("src.analysis.temporal.bar_chart") as mock_chart:
        analyse_weekday_distribution(df)

        ordered_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        expected = df["day_name"].value_counts().reindex(ordered_days)

        args, kwargs = mock_chart.call_args

        assert args[0].equals(expected)
        assert args[1] == "Collisions by Weekday (West Yorkshire)"
        assert args[2] == "Day of Week"
        assert args[3] == "Number of Collisions"
        assert kwargs["color"] == "darkorange"


def test_analyse_month_distribution_calls_bar_chart():
    df = pd.DataFrame({"month": [1, 1, 3]})

    with patch("src.analysis.temporal.bar_chart") as mock_chart:
        analyse_month_distribution(df)

        expected = df["month"].value_counts().sort_index()

        args, kwargs = mock_chart.call_args

        assert args[0].equals(expected)
        assert args[1] == "Collisions by Month (West Yorkshire)"
        assert args[2] == "Month"
        assert args[3] == "Number of Collisions"
        assert kwargs["color"] == "seagreen"


def test_run_temporal_suite_calls_all_three():
    df = pd.DataFrame({"hour": [1], "day_name": ["Monday"], "month": [1]})

    with (
        patch("src.analysis.temporal.analyse_hour_distribution") as h,
        patch("src.analysis.temporal.analyse_weekday_distribution") as w,
        patch("src.analysis.temporal.analyse_month_distribution") as m,
    ):
        run_temporal_suite(df)

        h.assert_called_once_with(df)
        w.assert_called_once_with(df)
        m.assert_called_once_with(df)
