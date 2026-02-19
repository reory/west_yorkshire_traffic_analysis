import pandas as pd
from src.charts import pie_chart, bar_chart
from src.mappings import (
casualty_class_labels, 
age_band_labels, 
gender_options
)

#print(silence debugging prints, turn on when ready)

def run_demographic_suite(vehicles_df, casualties_df):
    """Analyses the 'who' and the 'what' using linked data."""

    #print("Running Demographic & Vehicle Analysis...")

    # Driver Gender (from vehicle file)
    if not vehicles_df.empty and 'sex_of_driver' in vehicles_df.columns:
        gender_counts = vehicles_df["sex_of_driver"].map(gender_options).value_counts()
        pie_chart(gender_counts, "Driver Gender Distribution West Yorkshire",
                  pctdistance=1.0,
                  labeldistance=0.5,
                  colors=["#0698f8", "#f781a8", "#E2CC07FF"]
        )
        
    # Driver age (from vehicle.csv)
    if not vehicles_df.empty and 'age_band_of_driver' in vehicles_df.columns:

        # Filter out -1 (Missing data) for a cleaner graph.
        valid_ages = vehicles_df[vehicles_df['age_band_of_driver'] != -1].copy()

        # Map the integers to the readable strings
        valid_ages[
            'age_range'] = valid_ages['age_band_of_driver'].map(age_band_labels)
        
        # Count them , ensure they stay in the correct order 1-11.
        age_counts = valid_ages[
            'age_range'].value_counts().reindex(age_band_labels.values()).dropna()

        # Generate the chart.
        bar_chart(age_counts, "Collisions By Driver Age Band", 
                  "Age Group", "Count", color="#0698FA")

    # Casualty Class (from casualties.csv) - Driver, Passenger or Pedestrian.
    if not casualties_df.empty and 'casualty_class' in casualties_df.columns:
        class_counts = casualties_df[
            'casualty_class'].map(casualty_class_labels).value_counts()
        bar_chart(class_counts, "Casualty Type Distribution", 
                  "Type of Person", "Count", color="#5d88f4")
        
    # Top vehicle makes involved in accidents in West Yorkshire.
    if not vehicles_df.empty and 'generic_make_model' in vehicles_df.columns:

        # Filter out missing or unknown entries.
        # Explicity exclude the -1 as there was no data on which make of car 
        # that was involved in a collision.
        valid_vehicles = vehicles_df[
            (vehicles_df['generic_make_model'] != '-1') &
            (vehicles_df['generic_make_model'] != -1)
        ]

        # Get the top 10 most frequent makes/models.
        top_makes = valid_vehicles['generic_make_model'].value_counts().head(10)

        # Plot chart
        bar_chart(top_makes, "Top 10 Vehicle Makes in West Yorkshire Collisions",
                  "Vehicle Make/Model", "Total Incidents", color="#667294")
