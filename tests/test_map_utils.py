import pandas as pd

from src.map_utils import render_incident_map
from src.mappings import ui_mappings


def test_render_incident_map_handles_empty_dataframe():
    """Returns a folium map immediately when no data is supplied."""

    display_df = pd.DataFrame()
    cas_df = pd.DataFrame()
    veh_df = pd.DataFrame()

    result = render_incident_map(
        display_df,
        cas_df,
        veh_df,
        show_markers=True,
        show_heatmap=True,
        ui_mappings=ui_mappings,
    )

    assert result is not None


def test_render_incident_map_with_markers_and_heatmap():
    """Exercise the main rendering path."""

    display_df = pd.DataFrame(
        {
            "collision_index": ["A1"],
            "latitude": [53.8],
            "longitude": [-1.5],
            "collision_severity": [1],
            "weather_conditions": [1],
            "light_conditions": [1],
            "road_surface_conditions": [1],
            "road_type": [6],
            "urban_or_rural_area": [1],
            "special_conditions_at_site": [0],
            "number_of_vehicles": [1],
            "display_road_type": ["Single carriageway"],
            "date": ["2023-01-01"],
        }
    )

    cas_df = pd.DataFrame(
        {
            "collision_index": ["A1"],
            "sex_of_casualty": [1],
            "age_band_of_casualty": [5],
        }
    )

    veh_df = pd.DataFrame(
        {
            "collision_index": ["A1"],
            "generic_make_model": ["Ford Fiesta"],
        }
    )

    result = render_incident_map(
        display_df,
        cas_df,
        veh_df,
        show_markers=True,
        show_heatmap=True,
        ui_mappings=ui_mappings,
    )

    assert result is not None


def test_render_incident_map_uses_fallback_paths():
    """Exercise several fallback branches."""

    display_df = pd.DataFrame(
        {
            "collision_index": ["X1"],
            "latitude": [53.8],
            "longitude": [-1.5],
            "collision_severity": [3],
            "weather_conditions": [9],
            "light_conditions": [9],
            "road_surface_conditions": [9],
            "road_type": [15],
            "urban_or_rural_area": [2],
            "special_conditions_at_site": [9],
            "number_of_vehicles": [1],
            "date": ["2023-01-01"],
        }
    )

    cas_df = pd.DataFrame(
        columns=[
            "collision_index",
            "sex_of_casualty",
            "age_band_of_casualty",
        ]
    )

    veh_df = None

    result = render_incident_map(
        display_df,
        cas_df,
        veh_df,
        show_markers=False,
        show_heatmap=False,
        ui_mappings=ui_mappings,
    )

    assert result is not None
