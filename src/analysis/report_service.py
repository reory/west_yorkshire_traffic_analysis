import os
import shutil

from src.analysis.blackspots import identify_blackspots
from src.analysis.report_generator import generate_pdf_report
from src.analysis.summary_analysis import run_comprehensive_summary
from src.charts import generate_blackspots_chart


def build_report(
    accidents_df, 
    vehicles_df, 
    data_duration="Unknown", 
    chart_folder="temp_report"
):
    """Generate charts, summary and PDF report."""

    print("DEBUG: build_report started")
    print(f"SUMMARY RECORDS: {len(accidents_df)}")
    hotspots = identify_blackspots(accidents_df, top_n=5)
    print("\nDEBUG HOTSPOTS:")
    print(hotspots)

    if os.path.exists(chart_folder):
        shutil.rmtree(chart_folder)
    os.makedirs(chart_folder, exist_ok=True)

    print("DEBUG: hotspots complete")
    generate_blackspots_chart(
        accidents_df,
        chart_folder,
        hotspots_data=hotspots,
        data_duration=data_duration,
    )

    print("DEBUG: chart complete")
    report_content = run_comprehensive_summary(
        accidents_df,
        vehicles_df,
        chart_folder=chart_folder,
    )
    
    print("DEBUG: summary complete")
    # Add report metadata at the top of the PDF summary.
    report_content.insert(0, f"Analysis Period: {data_duration}")
    report_content.insert(1, "")

    print("DEBUG: calling PDF generator")
    return generate_pdf_report(
        report_content, 
        hotspots_list=hotspots,
        chart_folder=chart_folder,
    )