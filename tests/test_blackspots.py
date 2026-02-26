import pytest
import pandas as pd
from src.analysis.blackspots import identify_blackspots

def test_identify_blackspots_logic():
    """Test if the analyzer correctly counts and ranks accident sites."""

    # Create the fake data to test.
    # 3 accidents at site A, 1 at site B.
    data = {
        'location_easting_osgr': [100, 100, 100, 200],
        'location_northing_osgr': [100, 100, 100, 200],
        'latitude': [53.1, 53.1, 53.1, 53.2],
        'longitude': [-1.1, -1.1, -1.1, -1.2],
        'local_authority_district': [1, 1, 1, 1],
        'display_road_type': ['A-Road', 'A-Road', 'A-Road', 'B-Road']

    }

    df = pd.DataFrame(data)

    # Run the function
    # We expect Site A to be rank 1 because it has 3 incidents.
    results = identify_blackspots(df, min_accidents=1)

    # Assertions - checks to see if the expected results are true.
    assert len(results) > 0
    assert results[0]['count'] == 3 # The top spot should have 3 incidents.
    assert 'latitude' in results[0] # Ensure the keys needed for the map/pdf exists.