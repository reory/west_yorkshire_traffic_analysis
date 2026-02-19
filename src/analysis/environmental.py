import pandas as pd
from src.charts import bar_chart
from src.mappings import(
    weather_labels,
    light_labels,
    surface_labels,
    special_labels
)

#print(silence debugging prints, turn on when ready)

def analyse_weather_distribution(df):
    """Analyzes collisions based on weather (Rain, Snow, Icy, etc)"""
    df_local = df.copy()
    df_local["weather_label"] = df_local["weather_conditions"].map(weather_labels)

    counts = df_local["weather_label"].value_counts()

    bar_chart(
        counts,
        "Collisions by Weather Condition (West Yorkshire)",
        "Weather Condition",
        "Number of Collisions",
        color="#9b9030ff"
    )

# Collisions by Light Conditions
def analyse_light_condtions(df):
    """Analyse conditions based on Daylight vs Darkness."""
    light_data = df["light_conditions"].map(light_labels)
    light_counts = light_data.value_counts()

    bar_chart(
        light_counts,
        "Collisions by Light Conditions (West Yorkshire)",
        "Light Condition",
        "Number of Collisions",
        color="slateblue"
    )

# Collisions by Road Surface Conditions
def analyse_road_surface(df):
    """Analyzes if the road was Dry, Wet or Icy."""
    surface_data = df["road_surface_conditions"].map(surface_labels)
    surface_counts = surface_data.value_counts()

    bar_chart(
        surface_counts,
        "Collisions by Road Surface Conditions (West Yorkshire)",
        "Road Surface Condition",
        "Number of Collisions",
        color="#F87A1A"
    )

# 4I — Special Conditions at Site
def analyse_special_conditions(df):
    """Highlights site hazards like Roadworks or Oil, excluding 'normal'"""
    data = df["special_conditions_at_site"].map(special_labels)
    counts = data.value_counts()

    # Filter out "No special conditions" to see actual hazards.
    if "No special conditions" in counts:
        counts = counts.drop("No special conditions")

    if counts.empty:
        #print("No special hazards identified at sites")
        return

    bar_chart(
        counts,
        "Special hazards as site (Excluding normal conditions)",
        "Special Condition",
        "Number of Collisions",
        color="#5b0bf0"
    )

def run_environmental_suite(df):
    """Execute the environmental analysis."""
    analyse_weather_distribution(df)
    analyse_light_condtions(df)
    analyse_road_surface(df)
    analyse_special_conditions(df)