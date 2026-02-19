import pandas as pd
from src.mappings import(
    road_type_labels, road_class_labels, district_names
)

def load_linked_data(filepath, target_indices, index_col='collision_index'):
    """
    Loads a secondary/third CSV file (Vehicles or Casualties) and filters it.
    to keep ONLY the records matching the West Yorkshire accidents.
    """
    #print(f"Loading and linking {filepath}...")

    # Optimize: Only load relevant columns if file is huge.
    try:
        df = pd.read_csv(filepath, low_memory=False)

        #Standardize the index name if needed.
        if index_col not in df.columns and 'accident_index' in df.columns:
            df = df.rename(columns={'accident_index': index_col})

        # Filter: Keep only rows where the index is in the West Yorkshire list.
        filtered_df = df[df[index_col].isin(target_indices)]

        #print(f" > Found {len(filtered_df)} related records.")
        return filtered_df
    
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return pd.DataFrame() # Return empty if it fails.

def load_wy_data(path="data/accidents.csv"):

    # Load the dataset.
    df = pd.read_csv(path, low_memory=False)

    # Extract useful components from the date.
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # This removes any row where the date couldn't be parsed (NAT ones)
    df = df.dropna(subset=["date"])

    # Extract useful components from the year/month/day name.
    df["year"] = df["date"].dt.year #type:ignore
    df["month"] = df["date"].dt.month #type:ignore
    df["day_name"] = df["date"].dt.day_name() #type:ignore

    # Clean the 'time' column and extract the hour of the day.
    # Some rows may be missing or have malformed info. so we use errors='coerce'
    df["time"] = pd.to_datetime(df["time"], format="%H:%M", errors="coerce")

    # Extract the hour 0-23. This is crucial for time-of-day analysis.
    df["hour"] = df["time"].dt.hour #type:ignore

    # Mapping requires clean latitude and longitude coordinates.
    # Remove rows where latitude or longitude is missing.
    df = df.dropna(subset=["latitude", "longitude"])

    # human readable string across the whole dataset.
    df["road_type"] = df["road_type"].map(road_type_labels)

    # Map the road class (The rank)
    df["road_class_name"] = df["first_road_class"].map(road_class_labels)

    # Create the smart label - combining class and type of road.
    def identify_road(row):
        if row['road_class_name'] == "Motorway":

            # This turns Dual Carriageway into Motorway(Dual Carriageway)
            return f"Motorway({row['road_type']})"
        else:
            return row["road_type"]
    
    df["display_road_type"] = df.apply(identify_road, axis=1)

    # Apply filter to clean the new filtered data.
    df_filtered = df[df["local_authority_ons_district"].isin(district_names)]

    # How many motorways are in West Yorkshire.
    wy_motorways = len(df_filtered[df_filtered['first_road_class'] == 1])
    #print(f"Motorway accidents actually inside West Yorkshire: {wy_motorways}")

    return df_filtered

def get_data_period(df):
    """Returns a string describing the date range of the dataset."""
    
    if df.empty or 'date' not in df.columns:
        return "Unknown Period"
    
    start = df['date'].min().strftime("%d, %b, %Y")
    end = df['date'].max().strftime("%d, %b, %Y")

    return f"{start} to {end}"

