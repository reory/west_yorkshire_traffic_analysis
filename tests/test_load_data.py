import pandas as pd
from unittest.mock import patch
from src.load_data import load_linked_data, load_wy_data, get_data_period


def test_load_linked_data_filters_correctly():
    df_mock = pd.DataFrame({"collision_index": ["A", "B", "C"], "value": [1, 2, 3]})

    with patch("src.load_data.pd.read_csv", return_value=df_mock):
        result = load_linked_data("fake.csv", target_indices=["A", "C"])

        assert list(result["collision_index"]) == ["A", "C"]


def test_load_linked_data_renames_accident_index():
    df_mock = pd.DataFrame({"accident_index": ["X", "Y"], "value": [10, 20]})

    with patch("src.load_data.pd.read_csv", return_value=df_mock):
        result = load_linked_data("fake.csv", target_indices=["Y"])

        assert "collision_index" in result.columns
        assert list(result["collision_index"]) == ["Y"]


def test_load_linked_data_exception_returns_empty():
    with patch("src.load_data.pd.read_csv", side_effect=Exception("fail")):
        result = load_linked_data("bad.csv", target_indices=["A"])
        assert result.empty


def test_load_wy_data_full_cleaning():
    df_mock = pd.DataFrame(
        {
            "date": ["2023-01-01", "bad-date"],
            "time": ["12:30", "bad"],
            "latitude": [53.8, None],
            "longitude": [-1.5, -1.6],
            "road_type": [1, 2],
            "first_road_class": [1, 2],
            "local_authority_ons_district": ["E08000035", "E00000000"],
        }
    )

    with (
        patch("src.load_data.pd.read_csv", return_value=df_mock),
        patch("src.load_data.road_type_labels", {1: "Dual", 2: "Single"}),
        patch("src.load_data.road_class_labels", {1: "Motorway", 2: "A Road"}),
        patch("src.load_data.district_names", ["E08000035"]),
    ):
        result = load_wy_data("fake.csv")

        # Only the first row survives (valid date + lat/lon + district)
        assert len(result) == 1

        row = result.iloc[0]

        assert row["year"] == 2023
        assert row["month"] == 1
        assert row["day_name"] == "Sunday"
        assert row["hour"] == 12

        # Motorway logic
        assert row["road_class_name"] == "Motorway"
        assert row["display_road_type"] == "Motorway(Motorway)"


def test_get_data_period_normal():
    df = pd.DataFrame({"date": pd.to_datetime(["2023-01-01", "2023-01-10"])})

    result = get_data_period(df)
    assert result == "01, Jan, 2023 to 10, Jan, 2023"


def test_get_data_period_empty():
    df = pd.DataFrame()
    assert get_data_period(df) == "Unknown Period"


def test_get_data_period_missing_date_column():
    df = pd.DataFrame({"x": [1, 2]})
    assert get_data_period(df) == "Unknown Period"
