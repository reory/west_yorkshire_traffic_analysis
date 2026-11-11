from src.charts import bar_chart
from src.mappings import light_labels, special_labels, surface_labels, weather_labels

#print(silence debugging prints, turn on when ready)

def analyse_weather_distribution(df, chart_folder="output_charts"):
    """Analyses collisions based on weather (Rain, Snow, Icy, etc)"""

    # Prepare weather condition data
    df_local = df.copy()
    df_local["weather_label"] = df_local["weather_conditions"].map(weather_labels)
    counts = df_local["weather_label"].value_counts()

    bar_chart(
        counts,
        "Collisions by Weather Condition (West Yorkshire)",
        "Weather Condition",
        "Number of Collisions",
        color="#9b9030ff",
        chart_folder=chart_folder,
    )


def analyse_light_conditions(df, chart_folder="output_charts"):
    """Analyse conditions based on Daylight vs Darkness."""

    # Count lighting conditions frequencies
    light_data = df["light_conditions"].map(light_labels)
    light_counts = light_data.value_counts()

    bar_chart(
        light_counts,
        "Collisions by Light Conditions (West Yorkshire)",
        "Light Condition",
        "Number of Collisions",
        color="slateblue",
        chart_folder=chart_folder,
    )


def analyse_road_surface(df, chart_folder="output_charts"):
    """Analyses if the road was Dry, Wet or Icy."""

    # Calculate surface condition frequencies
    surface_data = df["road_surface_conditions"].map(surface_labels)
    surface_counts = surface_data.value_counts()

    bar_chart(
        surface_counts,
        "Collisions by Road Surface Conditions (West Yorkshire)",
        "Road Surface Condition",
        "Number of Collisions",
        color="#F87A1A",
        chart_folder=chart_folder,
    )


def analyse_special_conditions(df, chart_folder="output_charts"):
    """Highlights site hazards like Roadworks or Oil, excluding 'normal'"""

    # Calculate special condition frequencies
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
        color="#5b0bf0",
        chart_folder=chart_folder,
    )


def run_environmental_suite(df, chart_folder="output_charts"):
    """Execute the environmental analysis."""

    # Generate environmental analysis charts
    analyse_weather_distribution(df, chart_folder=chart_folder)
    analyse_light_conditions(df, chart_folder=chart_folder)
    analyse_road_surface(df, chart_folder=chart_folder)
    analyse_special_conditions(df, chart_folder=chart_folder)