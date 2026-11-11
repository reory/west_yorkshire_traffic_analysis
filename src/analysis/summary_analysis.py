from src.charts import pie_chart
from src.mappings import gender_options, light_labels, severity_labels, weather_labels

#print(silence debugging prints, turn on when ready)

def run_comprehensive_summary(
    df, 
    vehicles_df, 
    casualties_df,
    chart_folder="output_charts"
):
    """
    Generate summary statistics and supporting report content for the supplied
    accident and vehicle datasets.

    Returns a list of formatted report lines for PDF generation.
    """

    total_accidents = len(df)
    report_lines = []

    # Infrastructure Breakdown
    motorway_df = df[df["first_road_class"] == 1]
    motorway_count = len(motorway_df)
    motorway_pct = (motorway_count / total_accidents) * 100

    # Environmental Hazards
    # Identifying the 'typical' conditions for a West Yorkshire accident
    top_weather = df["weather_conditions"].mode()[0]
    top_light = df["light_conditions"].mode()[0]

    # Severity Analysis & Hazard Score
    # Mapping numbers (Fatal, Serious, Slight) from mappings.py
    severity_counts = df[
        "collision_severity"].value_counts().rename(index=severity_labels)

    # Calculate Hazard Score (Percentage of accidents that are Serious or Fatal)
    high_severity = severity_counts.get(
        "Fatal", 0) + severity_counts.get("Serious", 0)
    hazard_score = (high_severity / total_accidents) * 100

    # Driver and Vehicle intelligence.
    top_gender_text = "Unknown"
    top_vehicle_text = "Unknown"

    if not casualties_df.empty:

        raw_gender = casualties_df["sex_of_casualty"].mode()[0]
        top_gender_text = gender_options.get(raw_gender, "Unknown")

    if not vehicles_df.empty:

        # Get top vehicle make.
        valid_v = vehicles_df[vehicles_df["generic_make_model"] != "-1"]

        if not valid_v.empty:
            top_vehicle_text = valid_v["generic_make_model"].mode()[0]

    # Collect the data for the PDF.
    report_lines.append(f"REGIONAL HAZARD SCORE: {hazard_score:.1f}%")
    report_lines.append(f"TOTAL DATASET: {total_accidents} records analysed.")
    report_lines.append(f"MOTORWAY INCIDENTS: {motorway_count} incidents ({motorway_pct:.1f}% of total).")
    report_lines.append("") # Space in the PDF document.
    report_lines.append("PROFILED RISK GROUPS:")
    report_lines.append(f" - Predominant Casualty Gender: {top_gender_text}")
    report_lines.append(f" - Most Common Vehicle Model: {top_vehicle_text}")
    report_lines.append("") 
    report_lines.append("ENVIRONMENTAL PROFILE:")
    report_lines.append(f" - Predominant Weather: {weather_labels.get(top_weather, top_weather)}")
    report_lines.append(f" - Predominant Lighting: {light_labels.get(top_light, top_light)}")
    report_lines.append("")
    report_lines.append("SEVERITY PROFILE:")
    for sev, count in severity_counts.items():
        report_lines.append(f" - {sev}: {count}")
    report_lines.append("")

    # Generate severity distribution chart
    pie_chart(
        severity_counts,
        "Collision Severity Distribution West Yorkshire",
        pctdistance=0.7,
        colors=["#fa0202", "#fd7906", "#F9F906"],
        chart_folder=chart_folder,
    )

    return report_lines


#========================================================================
    # Generate the Final Report
    #print("\n" + "═" * 50)
    #print("WEST YORKSHIRE TRAFFIC INTELLIGENCE REPORT")
    #print("═" * 50)
    #for line in report_lines:
        #print(line)
    #print("=" * 50 + "\n")
#========================================================================

#========================================================================
    # Historical console reporting logic removed.
    # print(f"TOTAL DATASET: {total_accidents} records analysed.")
    # print(
    #     f"MOTORWAY SCOPE: {motorway_count} incidents" 
    #     f"({(motorway_count/total_accidents)*100:.1f}% of total)."
    # )

    # print("\nPROFILED RISK GROUPS:")
    # print(f" - Primary Driver Gender: {top_gender_text}")
    # print(f" - Most Frequent Vehicle: {top_vehicle_text}")

    # print("\nENVIRONMENTAL PROFILE:")
    # print(f" - Predominant Weather: {weather_map.get(top_weather, top_weather)}")
    # print(f" - Predominant Lighting: {light_map.get(top_light, top_light)}")

    # print("\nSEVERITY & RISK:")
    # for sev, count in severity_counts.items():
    #     print(f" - {sev}: {count}")

    # print(f"\nREGIONAL HAZARD SCORE: {hazard_score:.1f}%")
    # print(" (Percentage of total accidents resulting in Serious/Fatal outcomes)")
    # print("═" * 50 + "\n")
#================================================================================
   
