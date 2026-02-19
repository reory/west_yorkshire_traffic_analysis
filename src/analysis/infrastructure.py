import pandas as pd
from src.charts import bar_chart, pie_chart
from src.mappings import urban_rural_labels

def analyse_road_type_distribution(df):
    """Analyzes collisions by road layout (Roundabouts, Single carriageways, etc)"""

    counts = df["display_road_type"].value_counts()

    bar_chart(
        counts,
        "Collisions by Road Type (West Yorkshire)",
        "Road Type",
        "Number of Collisions",
        color="#56CF5AFF"
    )

# Urban/Rural x Speed Limit.
def analyse_urban_rural_proportion(df):
    """Compares the proportion of accidents in urban vs rural areas."""

    df_local = df.copy()
    df_local["area_label"] = df_local["urban_or_rural_area"].map(urban_rural_labels)
    counts = df_local["area_label"].value_counts()
    
    pie_chart(
        counts,
        "Proportion of Urban vs Rural Collisions (West Yorkshire)",
        pctdistance=0.8,
        labeldistance=1.0,
        colors=["#8cb49d", "#fd0707"]
    )

def analyse_speed_limit_distribution(df):
    """Visualizes the frequency of collisions at different speed limits."""
    
    counts = df["speed_limit"].value_counts().sort_index()

    bar_chart(
        counts,
        "Collisions by Speed Limit (West Yorkshire)",
        "Speed Limit (mph)",
        "Number of Collisions",
        color="#3cbaf0ff"
    )

def run_infrastructure_suite(df):
    """Executes the full infrastructure analysis."""
    analyse_road_type_distribution(df)
    analyse_speed_limit_distribution(df)
    analyse_urban_rural_proportion(df)
