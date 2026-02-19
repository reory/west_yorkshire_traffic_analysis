import webbrowser
import os
import folium
import time
import reverse_geocoder as rg # better than geopy to stop hitting apis.
from folium.plugins import MarkerCluster
from src.mappings import severity_labels

def get_address(lat, lon):
    """Translate the coordinates into a human readable street name. (OFFLINE)"""

    # Initiate the try block.
    try:
        # Add a timeout for web requests.
        results = rg.search((lat, lon))
        if results:
            area = results[0].get('name', 'Unknown Area')
            return area
    except Exception:
        return "Area Lookup Failed"
    return "Unknown Location"

def generate_severity_map(df, blackspots=None, output_path="collision_map.html"):
    """Creates an interactive cluster map of collisons."""

    # Initialize the map centered on Leeds area.
    m = folium.Map(
        location=[53.8008,-1.5491],
        zoom_start=10,
        tiles="cartodbpositron"
    )

    # Initialize the cluster group.
    marker_cluster = MarkerCluster().add_to(m)

    # Drop rows without coordinates to prevent errors.
    sample_df = df.dropna(subset=["latitude", "longitude"]).head(5000)

    for _, row in sample_df.iterrows():
        severity = severity_labels.get(row["collision_severity"], "Unknown")

        # Color logic for the pins on the map.
        # Motorway collisions stand out as red.
        if row["first_road_class"] == 1:
            pin_color = "red"
            pin_icon = "road"
        
        else:
            pin_color = "lightblue"
            pin_icon = "info-sign"

        # Safe access to display road type.
        road_type = row.get("display_road_type", "Standard Road")

        # Define popup content.
        popup_text = f"""
        <b>Severity:</b> {severity}<br>
        <b>Date:</b> {row['date']}<br>
        <b>Road Type:</b> {road_type}<br>
        """
    
        # Create the marker and add to the cluster.
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip="Click for details",
            icon=folium.Icon(color=pin_color, icon=pin_icon)
        ).add_to(marker_cluster)

    # Add high risk accident blackspots (OFFLINE Mode)
    if blackspots is not None:
        print("Mapping Priority Blackspots (Local Lookup)......")
        for i, spot in enumerate(blackspots, 1):
            
            lat = spot['latitude']
            lon = spot['longitude']
            count = spot['count']

            # Use new helper method
            street_name = get_address(lat, lon)

            # Create a label that explains the rank of the blackspot.
            # Rank 1-3 are the critical accident blackspots.
            rank_desc = "CRITICAL HAZARD" if i <= 3 else "High Risk Area"

            folium.CircleMarker(
                location=[lat, lon],
                radius=12,
                popup=folium.Popup(f"""
                    <div style="font-family: Arial; width: 200px;">
                        <b style="color: #CC0000;">RANK {i}: {rank_desc}</b><br><br>
                        <b>Location:</b><br>{street_name}<br><br>
                        <small style="color: #666;">GPS: {lat}, {lon}</small>
                    </div>
                """, max_width=300),
                tooltip=f"Rank {i}: {street_name} ({count} Incidents)",
                color="#CC0000",
                weight=4,
                fill=True,
                fill_color="white",
                fill_opacity=1.0
            ).add_to(m) # Added directly to map not the cluster.

    # Save the map path.
    m.save(output_path)

    # 2. Define the Dark Theme Legend HTML
    legend_html = '''
    <div id="wy-traffic-legend" style="position: fixed; 
    bottom: 30px; left: 30px; width: 260px; height: auto; 
    
    /* --- NEW COLOR STYLES --- */
    /* A nice 'lighter black' (dark charcoal) background with 90% opacity */
    background-color: rgba(40, 40, 40, 0.90); 
    /* Light off-white text color for readability */
    color: #f0f0f0;
    /* A slightly lighter gray border to match */
    border: 2px solid #777;
    /* A softer shadow for depth */
    box-shadow: 4px 4px 15px rgba(0,0,0,0.5);
    /* ------------------------ */
    
    z-index:999999; font-size:14px;
    padding: 15px;
    border-radius: 10px; 
    word-wrap: break-word;">
    
    <b style="font-size: 16px;">West Yorkshire Map Guide</b><br>
    <hr style="margin: 8px 0; border-color: #555;">
    
    <b>Cluster Volume (Density)</b><br>
    <div style="margin-top: 5px;">
        <span style="color:#50c878; font-size: 20px; vertical-align: middle;">●</span> 
        <span style="vertical-align: middle;">Low volume (&lt;10)</span><br>
        
        <span style="color:gold; font-size: 20px; vertical-align: middle;">●</span> 
        <span style="vertical-align: middle;">Medium volume (10-99)</span><br>
        
        <span style="color:orange; font-size: 20px; vertical-align: middle;">●</span> 
        <span style="vertical-align: middle;">High volume (100+)</span>
    </div>
    
    <hr style="margin: 12px 0; border-color: #555;">
    
    <b>Road Type (Zoomed In)</b><br>
    <div style="margin-top: 5px;">
        <span style="color:#4da6ff; font-size: 20px; vertical-align: middle;">●</span> 
        <span style="vertical-align: middle;">Standard Road</span><br>
        
        <span style="color:#ff4d4d; font-size: 20px; vertical-align: middle;">●</span> 
        <span style="vertical-align: middle;">Motorway</span>
    </div>
    </div>
    '''
    
    # 3. MANUAL INJECTION: Open the file and insert the HTML
    with open(output_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Find the closing body tag and insert the legend before it
    updated_html = html_content.replace("</body>", f"{legend_html}</body>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(updated_html)

    #print("Map and Legend generated successfully.")

    # This will open the map file in the default browser automatically.
    full_path = os.path.abspath(output_path)
    webbrowser.open(f"file://{full_path}")


