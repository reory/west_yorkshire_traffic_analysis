import numpy as np
import reverse_geocoder as rg  # offline tool for the blackspots coordinates.


def identify_blackspots(df, top_n=10, min_accidents=2):
    """Uses NumPy, Pandas and Geocoder to identify 
    high-frequency accident locations."""

    # Round coordinates to 2 decimal places (~1km precision)
    # This creates broader geographical clusters and highlights
    # recurring accident locations within the same local area.
    lats = np.round(df["latitude"].to_numpy(), 2)
    lons = np.round(df["longitude"].to_numpy(), 2)

    # Use numpy to find unique coordinate pairs and their counts.
    coords = np.column_stack((lats, lons))
    unique_coords, counts = np.unique(coords, axis=0, return_counts=True)

    # Sort by counts in descending order.
    sorted_indices = np.argsort(-counts)

    # Ensure we don't try to grab more blackspots than actually exist.
    actual_top_n = min(top_n, len(unique_coords))
    top_indices = sorted_indices[:actual_top_n]
    
    # Build a list of results.
    blackspots_results = []

    for i in top_indices:
        # Get specific coordinates.
        lat, lon = unique_coords[i]
        # Get specific count.
        current_count = counts[i]

        # Ask the offline database "Where is the this place from the lat,lon?"
        # Mode=1 means find the closest single match.
        results = rg.search((lat, lon), mode=1)

        # Results is a list of dictionaries.
        # Admin2 usually give "Leeds District", "Bradford District", WY.
        area_name = results[0]['admin2']
        
        # Get the most common road type at this specific spot for context.
        mask = (np.round(df["latitude"], 2) == lat) & (
            np.round(df["longitude"], 2) == lon)
        
        road_info = df[mask][
            "display_road_type"
            ].mode().iloc[0] if not df[mask].empty else "Unknown"
        
        # Create a label for the chart. 
        # This is a specific spot (site) at these coordinates.
        site_label = area_name

        # Build a dictionary
        blackspots_results.append(
            {
                "latitude": lat,
                "longitude": lon,
                "area": area_name,
                "site_label": site_label,
                "count": int(current_count),
                "road_type": road_info,
            }
        )
    
    return [
        spot
        for spot in blackspots_results
        if spot["count"] >= min_accidents
    ]

    