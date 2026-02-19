import pandas as pd
from src.charts import bar_chart

def analyse_hour_distribution(df):
    """Shows when collisions peak during the day (Rush hour, etc)"""
    hour_counts = df["hour"].value_counts().sort_index()

    bar_chart(
        hour_counts,
        "Collisions by Hour of Day (West Yorkshire)",
        "Hour(24h)",
        "Number of Collisions",
        color="steelblue"
    )

def analyse_weekday_distribution(df):
    """Show which days are the most dangerous to have a collision."""

    # Ensure your data has a 'day_of_week' column or use the index.
    weekday_counts = df["day_name"].value_counts()

    ordered_days = [
        "Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", 
        "Sunday"
    ]
    weekday_counts = weekday_counts.reindex(ordered_days)

    bar_chart(
        weekday_counts,
        "Collisions by Weekday (West Yorkshire)",
        "Day of Week",
        "Number of Collisions",
        color="darkorange"
    )

# 4C — Collisions by Month
def analyse_month_distribution(df):
    """Analyzes seasonal trends across the year."""

    # Sort index keeps months in order (1-12)
    month_counts = df["month"].value_counts().sort_index()

    bar_chart(
        month_counts,
        "Collisions by Month (West Yorkshire)",
        "Month",
        "Number of Collisions",
        color="seagreen"
    )

def run_temporal_suite(df):
    """Executes the full time series analysis."""
    analyse_hour_distribution(df)
    analyse_weekday_distribution(df)
    analyse_month_distribution(df)