import os
import shutil

from src.analysis.blackspots import identify_blackspots
from src.analysis.environmental import (
    analyse_light_conditions,
    analyse_road_surface,
    analyse_special_conditions,
    analyse_weather_distribution,
)
from src.analysis.geography import analyse_severity_by_district
from src.analysis.report_generator import generate_pdf_report
from src.analysis.summary_analysis import run_comprehensive_summary
from src.charts import generate_blackspots_chart


def build_report(
    accidents_df, 
    vehicles_df,
    casualties_df,
    data_duration="Unknown", 
    chart_folder="temp_report"
):
    """Generate charts, summary and PDF report."""

    hotspots = identify_blackspots(accidents_df, top_n=5)

    # Recreate chart output folder
    if os.path.exists(chart_folder):
        shutil.rmtree(chart_folder)
    os.makedirs(chart_folder, exist_ok=True)

    # Generate blackspot analysis chart
    generate_blackspots_chart(
        accidents_df,
        chart_folder,
        hotspots_data=hotspots,
        data_duration=data_duration,
    )

    # Environmental intelligence charts.
    analyse_weather_distribution(
        accidents_df,
        chart_folder=chart_folder,
    )

    analyse_light_conditions(
        accidents_df,
        chart_folder=chart_folder,
    )

    analyse_road_surface(
        accidents_df,
        chart_folder=chart_folder,
    )

    analyse_special_conditions(
        accidents_df,
        chart_folder=chart_folder,
    )

    # Geographical intelligence charts.
    analyse_severity_by_district(
        accidents_df,
        chart_folder=chart_folder,
    )

    report_content = run_comprehensive_summary(
        accidents_df,
        vehicles_df,
        casualties_df,
        chart_folder=chart_folder,
    )
    
    # Add report metadata at the top of the PDF summary.
    report_content.insert(0, f"Analysis Period: {data_duration}")
    report_content.insert(1, "")

    return generate_pdf_report(
        report_content, 
        hotspots_list=hotspots,
        chart_folder=chart_folder,
    )