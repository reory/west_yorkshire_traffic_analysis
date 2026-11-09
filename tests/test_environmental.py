import pandas as pd

from src.analysis import environmental


def test_analyse_weather_distribution_calls_bar_chart(mocker):
    """Ensure weather analysis generates a chart."""

    mock_chart = mocker.patch(
        "src.analysis.environmental.bar_chart"
    )

    df = pd.DataFrame(
        {
            "weather_conditions": [1, 2, 2]
        }
    )

    environmental.analyse_weather_distribution(df)

    mock_chart.assert_called_once()

    args = mock_chart.call_args[0]

    assert args[1] == "Collisions by Weather Condition (West Yorkshire)"
    assert args[2] == "Weather Condition"
    assert args[3] == "Number of Collisions"


def test_analyse_light_conditions_calls_bar_chart(mocker):
    """Ensure light condition analysis generates a chart."""

    mock_chart = mocker.patch(
        "src.analysis.environmental.bar_chart"
    )

    df = pd.DataFrame(
        {
            "light_conditions": [1, 4, 5]
        }
    )

    environmental.analyse_light_condtions(df)

    mock_chart.assert_called_once()

    args = mock_chart.call_args[0]

    assert args[1] == "Collisions by Light Conditions (West Yorkshire)"
    assert args[2] == "Light Condition"
    assert args[3] == "Number of Collisions"


def test_analyse_road_surface_calls_bar_chart(mocker):
    """Ensure road surface analysis generates a chart."""

    mock_chart = mocker.patch(
        "src.analysis.environmental.bar_chart"
    )

    df = pd.DataFrame(
        {
            "road_surface_conditions": [1, 2, 4]
        }
    )

    environmental.analyse_road_surface(df)

    mock_chart.assert_called_once()

    args = mock_chart.call_args[0]

    assert args[1] == "Collisions by Road Surface Conditions (West Yorkshire)"
    assert args[2] == "Road Surface Condition"
    assert args[3] == "Number of Collisions"


def test_analyse_special_conditions_calls_bar_chart(mocker):
    """Ensure special hazards are charted when present."""

    mock_chart = mocker.patch(
        "src.analysis.environmental.bar_chart"
    )

    df = pd.DataFrame(
        {
            "special_conditions_at_site": [4, 6, 7]
        }
    )

    environmental.analyse_special_conditions(df)

    mock_chart.assert_called_once()

    args = mock_chart.call_args[0]

    assert args[1] == "Special hazards as site (Excluding normal conditions)"
    assert args[2] == "Special Condition"
    assert args[3] == "Number of Collisions"


def test_analyse_special_conditions_returns_when_no_hazards(mocker):
    """No chart should be generated if all rows are normal conditions."""

    mock_chart = mocker.patch(
        "src.analysis.environmental.bar_chart"
    )

    df = pd.DataFrame(
        {
            "special_conditions_at_site": [0, 0, -1]
        }
    )

    environmental.analyse_special_conditions(df)

    mock_chart.assert_not_called()


def test_run_environmental_suite_calls_all_analyses(mocker):
    """Ensure the environmental suite executes all analyses."""

    weather = mocker.patch(
        "src.analysis.environmental.analyse_weather_distribution"
    )

    light = mocker.patch(
        "src.analysis.environmental.analyse_light_condtions"
    )

    surface = mocker.patch(
        "src.analysis.environmental.analyse_road_surface"
    )

    special = mocker.patch(
        "src.analysis.environmental.analyse_special_conditions"
    )

    environmental.run_environmental_suite(pd.DataFrame())

    weather.assert_called_once()
    light.assert_called_once()
    surface.assert_called_once()
    special.assert_called_once()