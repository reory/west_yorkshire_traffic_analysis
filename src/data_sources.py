"""Create a central data source configuration."""

from pathlib import Path

# Base data directory
DATA_ROOT = Path("data")

# Dataset file definitions by year
DATA_SOURCES = {
    2024: {
        "accidents": DATA_ROOT / "2024" / "accidents.csv",
        "vehicles": DATA_ROOT / "2024" / "vehicles.csv",
        "casualties": DATA_ROOT / "2024" / "casualties.csv",
    },

    2025: {
        "accidents": DATA_ROOT / "2025" / "accidents.csv",
        "vehicles": DATA_ROOT / "2025" / "vehicles.csv",
        "casualties": DATA_ROOT / "2025" / "casualties.csv",
    },
}