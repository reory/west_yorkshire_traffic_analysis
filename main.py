"""
Run the complete West Yorkshire traffic analysis workflow.

Loads source datasets, executes all analysis modules, generates charts,
identifies blackspots, creates interactive maps, and exports a PDF report.
"""

import logging
import os
import time

import matplotlib.pyplot as plt
import pandas as pd

from src.analysis.blackspots import identify_blackspots
from src.analysis.demographics import run_demographic_suite
from src.analysis.environmental import run_environmental_suite
from src.analysis.geography import run_geographical_suite
from src.analysis.infrastructure import run_infrastructure_suite
from src.analysis.mapping import generate_severity_map
from src.analysis.report_service import build_report
from src.analysis.temporal import run_temporal_suite
from src.data_sources import DATA_SOURCES
from src.load_data import get_data_period, load_linked_data, load_wy_data

plt.style.use("grayscale")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Change this value to run a different dataset year.
ANALYSIS_YEAR = 2025

def main():
    """Execute the complete West Yorkshire traffic analysis workflow."""

    try:
        source = DATA_SOURCES[ANALYSIS_YEAR]

        df = load_wy_data(
            source["accidents"]
        )
    except (
        FileNotFoundError,
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
    ):
        print("Error: No data loaded. Please check the file path.")
        return

    if df is None or df.empty:
        print("Error: No data loaded. Please check the file path.")
        return

    data_duration = get_data_period(df)

    # Identify the top accident blackspots for mapping/reporting.
    hotspots = identify_blackspots(df, top_n=5)

    # Load linked datasets.
    wy_indices = df["collision_index"].unique()

    vehicles_df = load_linked_data(
        source["vehicles"],
        wy_indices,
    )

    casualties_df = load_linked_data(
        source["casualties"],
        wy_indices,
    )

    print(f"Running analysis for {ANALYSIS_YEAR}")
    start_time = time.time()

    # Execute analysis suites and generate charts.
    run_geographical_suite(df)
    run_temporal_suite(df)
    run_infrastructure_suite(df)
    run_environmental_suite(df)
    run_demographic_suite(
        vehicles_df,
        casualties_df,
    )

    # Generate interactive Folium map.
    print("Generating Interactive Map...")
    generate_severity_map(
        df,
        blackspots=hotspots,
    )

    # Generate charts, summary, and PDF report.
    build_report(
        df,
        vehicles_df,
        casualties_df,
        data_duration,
    )

    # Calculate processing time
    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print(
        f"\nAnalysis complete! "
        f"Total processing time: {duration} seconds"
    )

    # Final chart sanity check.
    generated_files = os.listdir("output_charts")

    chart_count = len(
        [
            f
            for f in generated_files
            if f.endswith(".png")
        ]
    )

    if chart_count < 16:
        print(
            "⚠️ WARNING: "
            "Some charts are missing. "
            "Check for duplicate titles!"
        )
    else:
        print("✅ All systems go! The folder is full.")


if __name__ == "__main__":
    main()