import os
import pandas as pd
from unittest.mock import patch, MagicMock
from src.charts import (
    bar_chart,
    stacked_bar_chart,
    pie_chart,
    generate_blackspots_chart,
)


def test_bar_chart_saves_correct_file():
    series = pd.Series([1, 2, 3], index=["A", "B", "C"])

    with patch("src.charts.plt") as mock_plt:
        mock_fig = MagicMock()
        mock_plt.figure.return_value = mock_fig

        bar_chart(series, "Test Chart (Example)", "X", "Y", color="red")

        expected_filename = "Test_Chart_Example.png"
        expected_path = os.path.join("output_charts", expected_filename)

        mock_plt.savefig.assert_called_once_with(expected_path)
        mock_plt.close.assert_called_once()


def test_stacked_bar_chart_saves_file():
    df = pd.DataFrame({"Fatal": [1], "Serious": [2]})

    with (
        patch("src.charts.plt") as mock_plt,
        patch.object(pd.DataFrame, "plot") as mock_plot,
    ):
        stacked_bar_chart(df, "Severity Breakdown", "X", "Y", ["red", "orange"])

        expected_filename = "Severity_Breakdown.png"
        expected_path = os.path.join("output_charts", expected_filename)

        mock_plot.assert_called_once()

        actual_path = mock_plt.savefig.call_args[0][0]

        assert os.path.normpath(actual_path) == os.path.normpath(expected_path)

        mock_plt.close.assert_called_once()


def test_pie_chart_saves_file():
    series = pd.Series([50, 50], index=["A", "B"])

    with patch("src.charts.plt") as mock_plt:
        pie_chart(series, "Pie Chart (Test)", colors=["red", "blue"])

        expected_filename = "Pie_Chart_Test.png"
        expected_path = os.path.join("output_charts", expected_filename)

        mock_plt.savefig.assert_called_once_with(expected_path)
        mock_plt.close.assert_called_once()


def test_blackspots_chart_no_data():
    with patch("src.charts.plt") as mock_plt:
        generate_blackspots_chart(None, "charts", hotspots_data=None)
        mock_plt.figure.assert_not_called()


def test_blackspots_chart_generates_file():
    hotspots = [
        {"area": "Leeds", "road_type": "A Road", "count": 12},
        {"area": "Bradford", "road_type": "Motorway", "count": 20},
    ]

    with patch("src.charts.plt") as mock_plt:
        generate_blackspots_chart(
            None, "charts", hotspots_data=hotspots, data_duration="2020-2023"
        )

        expected_path = os.path.join("charts", "blackspot_priority_analysis.png")

        mock_plt.savefig.assert_called_once_with(expected_path, dpi=300)
        mock_plt.close.assert_called_once()
