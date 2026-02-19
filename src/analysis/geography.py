import pandas as pd
import matplotlib.pyplot as plt
from src.charts import pie_chart, bar_chart, stacked_bar_chart
from src.mappings import severity_labels, district_names

#Below def method has already been taken care of.
# Severity Distribution
# def analyse_overall_severity(df):
#     """General overview of how dangerous the accidents are across WY."""
#     severity_data = df["collision_severity"].map(severity_labels)
#     severity_counts = severity_data.value_counts()

#     pie_chart(
#         severity_counts,
#         "Collision Severity Distribution (West Yorkshire)",
#         colors=["#e74c3c", "#f39c12", "#f1c40f"],
#         pctdistance=0.8,
#         labeldistance=1.0
#     )

def analyse_severity_by_district(df):
    """
    Compares the accident count and severity levels across the
    5 West Yorkshire districts.
    """

    df_local = df.copy()

    # Map the ONS codes and severity levels using your mappings.py
    df_local[
        "district"] = df_local[
        "local_authority_ons_district"].map(district_names)
    df_local["severity"] = df_local["collision_severity"].map(severity_labels)

    # Create a cross tabulation(counts of severity per district)
    # This turns the data into a format for a stacked bar chart.
    district_comparison = pd.crosstab(
        df_local["district"],
        df_local["severity"])

    # Ensure the columns are in a logical severity order.
    column_order = ["Fatal", "Serious", "Slight"]

    district_comparison = district_comparison.reindex(
        columns=[c for c in column_order if c in district_comparison.columns])
    
    # Plotting the stacked bar chart.
    stacked_bar_chart(
        district_comparison,
        "Accident Severity Breakdown by West Yorkshire District",
        "District",
        "Number of Accidents",
        ["#e74c3c", "#f39c12", "#f1c40f"]
    )

def run_geographical_suite(df):
    """Execute the geographical analysis."""
    #analyse_overall_severity(df)
    analyse_severity_by_district(df)
    

