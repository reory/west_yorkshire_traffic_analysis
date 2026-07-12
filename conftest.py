import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def sample_traffic_data():
    """
    A reusable fixture that provides dummy traffic data for tests files.
    Instead of recreating mock data in test_charts.py and test_temporal.py,
    you can just pass 'sample_traffic_data' as an argument to any test function.
    """
    return [
        {"location": "Leeds Center", "blackspot": True, "accidents": 12, "year": 2023},
        {"location": "Wakefield Road", "blackspot": False, "accidents": 2, "year": 2023},
        {"location": "Bradford Ring Road", "blackspot": True, "accidents": 15, "year": 2024}
    ]