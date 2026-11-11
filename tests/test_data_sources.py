from pathlib import Path

from src.data_sources import DATA_SOURCES


def test_supported_years():
    """Tests configured dataset years."""

    assert set(DATA_SOURCES.keys()) == {2024, 2025}


def test_required_files_exist():
    """Validates dataset source structure."""

    required = {
        "accidents",
        "vehicles",
        "casualties",
    }

    for source in DATA_SOURCES.values():
        assert set(source.keys()) == required

        for path in source.values():
            assert isinstance(path, Path)