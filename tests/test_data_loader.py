import pytest
import pandas as pd
from src.load_data import load_wy_data, get_data_period, load_linked_data

def test_load_wy_data_cleaning(tmp_path):
    """Test that coordinates and dates are cleaned and mapped correctly."""

    # Creat a temporary CSV file for testing only.
    d = tmp_path / "test_accidents.csv"

    # Build the test dict.
    data = {
        'collisions_index': ['A1', 'B2', 'C3'],
        'date': ['2023-01-01', '2023-01-02', 'Invalid-Date'],
        'time': ['14:30', '06:15', '13:45'],
        'latitude': [53.8, 53.9, None], # A missing coordinate (mix it up)
        'longitude': [-1.5, -1.6, -1.7],
        'local_authority_ons_district': ["E08000035", "E08000035", "E08000035"],
        'road_type': [4, 6, 3],
        'first_road_class': [1, 3, 3]
    }

    pd.DataFrame(data).to_csv(d, index=False)

    # Run the file.
    df = load_wy_data(str(d))
    
    # Assertions.
    # We started with 3 rows. One has a bad date, one has a missing latitude.
    # Only 1 row (B2) should survive both drops (dropna date AND dropna lat/lon).
    # Actually, A1 and B2 have valid dates and lats. C3 fails both.
    assert len(df) == 2
    assert df.iloc[0]['hour'] == 14
    assert df.iloc[0]['display_road_type'] == 'Motorway(Motorway)'
    assert df.iloc[1]['road_class_name'] == 'A'

def test_get_data_period_empty():
    """Ensures the test can handle empty data frames."""

    df = pd.DataFrame()
    assert get_data_period(df) == 'Unknown Period'