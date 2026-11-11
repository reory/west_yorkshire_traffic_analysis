from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.analysis.mapping import generate_severity_map, get_address


def test_get_address_success():
    """Tests successful area lookup."""

    with patch("src.analysis.mapping.rg.search") as mock_search:
        mock_search.return_value = [{"name": "Leeds"}]

        result = get_address(53.8, -1.5)
        assert result == "Leeds"


def test_get_address_empty_result():
    """Tests empty lookup results."""

    with patch("src.analysis.mapping.rg.search") as mock_search:
        mock_search.return_value = []

        result = get_address(53.8, -1.5)
        assert result == "Unknown Location"


def test_get_address_exception():
    """Tests lookup failure handling."""

    with patch(
        "src.analysis.mapping.rg.search", side_effect=ValueError("bad_coordinates")):
        result = get_address(53.8, -1.5)
        assert result == "Area Lookup Failed"


def test_get_address_unexpected_exception_propagates():
    """Tests unexpected exception propagation."""

    with (
        patch(
            "src.analysis.mapping.rg.search", 
            side_effect=RuntimeError("totally unexpected")
        ),
        pytest.raises(RuntimeError),
    ):
        get_address(53.8, -1.5)


def test_generate_severity_map_basic():
    """Tests basic map generation."""

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
    ):
        # Mock file read/write
        mock_open.return_value.__enter__.return_value.read.return_value = (
            "<body></body>"
        )
        generate_severity_map(df, blackspots=None, output_path="test.html")

        mock_map.save.assert_called_once_with("test.html")


def test_generate_severity_map_motorway_pin_colour():
    """Tests motorway marker styling."""

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
        patch("src.analysis.mapping.folium.Icon") as mock_icon,
        patch("src.analysis.mapping.folium.Marker"),
    ):
        generate_severity_map(df, blackspots=None)

        # motorway → red + road icon
        mock_icon.assert_called_with(color="red", icon="road")


def test_generate_severity_map_blackspots():
    """Tests blackspot marker creation."""

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
    ):
        generate_severity_map(df, blackspots=blackspots)

        mock_circle.assert_called()


def test_generate_severity_map_injects_referrer_meta(tmp_path):
    """Test referrer policy injection."""

    df = pd.DataFrame(
        {
            "latitude": [53.8],
            "longitude": [-1.4],
            "collision_severity": [2],
            "first_road_class": [4],
            "date": ["2025-01-04"],
            "display_road_type": ["A Road"],
        }
    )

    output_path = tmp_path / "test_map.html"

    generate_severity_map(
        df,
        blackspots=None,
        output_path=output_path,
    )

    html= output_path.read_text(encoding="utf-8")

    assert (
        '<meta name="referrer" '
        'content="strict-origin-when-cross-origin">'
    ) in html
