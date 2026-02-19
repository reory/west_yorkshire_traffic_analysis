import matplotlib.pyplot as plt
plt.style.use('grayscale')
import time
import os
from src.load_data import load_wy_data, load_linked_data, get_data_period
from src.charts import generate_blackspots_chart

from src.analysis.geography import run_geographical_suite
from src.analysis.environmental import run_environmental_suite
from src.analysis.infrastructure import run_infrastructure_suite
from src.analysis.temporal import run_temporal_suite
from src.analysis.mapping import generate_severity_map
from src.analysis.summary_analysis import run_comprehensive_summary
from src.analysis.blackspots import identify_blackspots
from src.analysis.demographics import run_demographic_suite
from src.analysis.report_generator import generate_pdf_report

def main():
    """Load the data (West Yorkshire filtered)"""
    
    #print("Loading West Yorkshire collison data...")
    df = load_wy_data("data/accidents.csv")

    if df is None or df.empty:
        # Error notification.
        print("Error: No data loaded. Please check the file path.")
        return

    # Get the duration.
    data_duration = get_data_period(df)
    #print(f"Analyzing data from: {data_duration}")

    # This now returns a list of dictionaries.
    hotspots = identify_blackspots(df, top_n=5)

    # Print the results for verification.
    #print("\n" + "😊" * 17)
    #print("🌍 OFFLINE GEO-LOOKUP SUCCESSFUL")
    #print("" + "😊" * 17)

    for i, spot in enumerate(hotspots, 1):
        #print(f"{i}. {spot['site_label']} | {spot['road_type']})")
        #print(f"   Coords: {spot['latitude']}, {spot['longitude']}")
        #print(f"   Total Incidents: {spot['count']}")
        print("-" * 30)

    # Link the new files to run after the main accidents csv file.
    wy_indices = df['collision_index'].unique()
    vehicles_df = load_linked_data("data/vehicles.csv", wy_indices)
    casualties_df = load_linked_data("data/casualties.csv", wy_indices)

    if df is None or df.empty:
        # Error notification.
        print("Error: No data loaded. Please check the file path.")
        return
    
    #print(f"Data loaded successfully. Analysing {len(df)} records...\n")
    start_time = time.time()

    # Execute analysis suites. Print charts to folder.
    #print("Running full analysis suites(Saving charts to folder)...")
    run_geographical_suite(df)
    run_temporal_suite(df)
    run_infrastructure_suite(df)
    run_environmental_suite(df)
    run_demographic_suite(vehicles_df, casualties_df)

    # Print the 5 accident blackspots chart.
    generate_blackspots_chart(
        df, "output_charts", hotspots_data=hotspots, data_duration=data_duration)

    # Run the summary
    report_content = run_comprehensive_summary(df, vehicles_df)

    # Insert the duration into the list for the PDF.
    report_content.insert(0, f"Analysis Period: {data_duration}")
    report_content.insert(1, "") # Add a blank space for better look on pdf.
    
    # Print Folium map - this will open in the browser.
    print("Generating Interactive Map...")
    generate_severity_map(df, blackspots=hotspots)

    # Final summary report.
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    #print(f"\n Analysis complete! Total processing time: {duration} seconds")
    
    # At the very end of Main.py
    generated_files = os.listdir("output_charts")
    chart_count = len([f for f in generated_files if f.endswith('.png')])

    #print("-" * 30)
    #print(f"📊 FINAL SANITY CHECK:")
    #print(f"Total Charts Expected: 16")
    #print(f"Total Charts Found:    {chart_count}")
    #print("-" * 30)

    if chart_count < 16:
        print("⚠️ WARNING: Some charts are missing. Check for duplicate titles!")
    else:
        print("✅ All systems go! The folder is full.")

    # Generate the PDF file.
    generate_pdf_report(report_content, hotspots_list=hotspots)

if __name__ == "__main__":
    main()
