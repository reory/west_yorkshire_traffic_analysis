import pandas as pd
from unittest.mock import patch, MagicMock
from src.analysis.mapping import get_address, generate_severity_map


def test_get_address_success():

    with patch("src.analysis.mapping.rg.search") as mock_search:
        mock_search.return_value = [{"name": "Leeds"}]

        result = get_address(53.8, -1.5)
        assert result == "Leeds"


def test_get_address_empty_result():

    with patch("src.analysis.mapping.rg.search") as mock_search:
        mock_search.return_value = []

        result = get_address(53.8, -1.5)
        assert result == "Unknown Location"


def test_get_address_exception():

    with patch("src.analysis.mapping.rg.search", side_effect=Exception("fail")):
        result = get_address(53.8, -1.5)
        assert result == "Area Lookup Failed"


def test_generate_severity_map_basic():

    df = pd.DataFrame(
        {
            "latitude": [53.8],
            "longitude": [-1.5],
            "collision_severity": [1],
            "first_road_class": [2],
            "date": ["2026-01-06"],
            "display_road_type": ["A Road"],
        }
    )

    mock_map = MagicMock()
    mock_map.save = MagicMock()

    with (
        patch("src.analysis.mapping.folium.Map", return_value=mock_map),
        patch("src.analysis.mapping.MarkerCluster"),
        patch("src.analysis.mapping.folium.Marker"),
        patch("src.analysis.mapping.folium.Popup"),
        patch("src.analysis.mapping.folium.Icon"),
        patch("src.analysis.mapping.open", create=True) as mock_open,
        patch("src.analysis.mapping.webbrowser.open") as mock_web,
    ):
        # Mock file read/write
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "<body></body>"
        )
        generate_severity_map(df, blackspots=None, output_path="test.html")

        mock_map.save.assert_called_once_with("test.html")
        mock_web.assert_called_once()


def test_generate_severity_map_motorway_pin_color():
    df = pd.DataFrame(
        {
            "latitude": [53.8],
            "longitude": [-1.5],
            "collision_severity": [1],
            "first_road_class": [1],  # motorway
            "date": ["2023-01-01"],
            "display_road_type": ["Motorway(Motorway)"],
        }
    )

    with (
        patch("src.analysis.mapping.folium.Map"),
        patch("src.analysis.mapping.MarkerCluster"),
        patch("src.analysis.mapping.folium.Popup"),
        patch("src.analysis.mapping.open", create=True),
        patch("src.analysis.mapping.webbrowser.open"),
        patch("src.analysis.mapping.folium.Icon") as mock_icon,
        patch("src.analysis.mapping.folium.Marker"),
    ):
        generate_severity_map(df, blackspots=None)

        # motorway → red + road icon
        mock_icon.assert_called_with(color="red", icon="road")


def test_generate_severity_map_blackspots():
    df = pd.DataFrame(
        {
            "latitude": [53.8],
            "longitude": [-1.5],
            "collision_severity": [1],
            "first_road_class": [2],
            "date": ["2023-01-01"],
            "display_road_type": ["A Road"],
        }
    )

    blackspots = [{"latitude": 53.7, "longitude": -1.4, "count": 12}]

    with (
        patch("src.analysis.mapping.folium.Map"),
        patch("src.analysis.mapping.MarkerCluster"),
        patch("src.analysis.mapping.folium.CircleMarker") as mock_circle,
        patch("src.analysis.mapping.get_address", return_value="Test Street"),
        patch("src.analysis.mapping.open", create=True),
        patch("src.analysis.mapping.webbrowser.open"),
    ):
        generate_severity_map(df, blackspots=blackspots)

        mock_circle.assert_called()
