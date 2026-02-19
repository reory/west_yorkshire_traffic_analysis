import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd

def render_incident_map(display_df, cas_df, veh_df, show_blackspots, ui_mappings):
    """
    Handles all map rendering logic, including markers and heatmap overlays.
    'mappings' should be a dictionary containing all your label dictionaries.
    """
    
    # Create the base map centered on West Yorkshire
    m = folium.Map(
        location=[53.8008, -1.5491], 
        zoom_start=10, 
        tiles='CartoDB positron'
    )
    
    if display_df.empty:
        return m

    # Pre-index casualties for lightning-fast lookup in the loop
    cas_indexed = cas_df.set_index('collision_index')

    # 1. Add Heatmap Layer (if toggled)
    if show_blackspots:
        heat_data = display_df[['latitude', 'longitude']].values.tolist()
        HeatMap(
            heat_data,
            radius=20,
            blur=20,
            min_opacity=0.4,
            gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
        ).add_to(m)

    # 2. Add Marker Cluster Layer
    marker_cluster = MarkerCluster().add_to(m)

    def get_marker_color(severity_code):
        if severity_code == 1: return 'red'
        if severity_code == 2: return 'orange'
        return 'yellow'

    # Loop through incidents (capped at 2500 for performance)
    for idx, row in display_df.head(2500).iterrows():
        this_id = row['collision_index']
        
        # Casualty/Gender/Age Lookup
        try:
            accident_casualties = pd.DataFrame(cas_indexed.loc[[this_id]])

            # Combine Gender and Age for each person involved.
            cas_details = []
            for _, c_row in accident_casualties.iterrows():
                g = ui_mappings['gender'].get(int(c_row['sex_of_casualty']), 'Unknown')
                age_code = int(c_row['age_band_of_casualty'])
                a = ui_mappings['age_choice'].get(age_code, 'Age Unknown')
                cas_details.append(f"{g} ({a})")
            
            casualty_summary = ", ".join(set(cas_details))
        except KeyError:
            casualty_summary = 'Not Recorded'

        # Vehicle lookup
        try:
            accident_vehicles = veh_df[veh_df['collision_index'] == this_id]

            veh_details = []
            for _, v_row in accident_vehicles.iterrows():
                # Grab the make and model of the vehicle from the CSV file.
                make = v_row.get('generic_make_model', 'Unknown Make')
                veh_details.append(make)

            vehicle_summary = ", ".join(set(veh_details)) if veh_details else 'Unknown Vehicle'
        except Exception:
            vehicle_summary = 'Vehicle Data Missing'

        # Translate codes using our mappings
        sev = ui_mappings['severity'].get(int(row['collision_severity']), 'Unknown')
        weather = ui_mappings['weather'].get(int(row['weather_conditions']), 'Unknown')
        light = ui_mappings['light'].get(int(row['light_conditions']), 'Unknown')
        surface = ui_mappings['surface'].get(int(row['road_surface_conditions']), 'Unknown')
        if 'display_road_type' in row and pd.notna(row['display_road_type']):
            road = row['display_road_type']
        else:
            # Fallback to the dictionary lookup using the numeric code
            raw_code = int(row['road_type'])
            road = ui_mappings['road_type'].get(raw_code, 'Unknown')
        area = ui_mappings['area'].get(int(row['urban_or_rural_area']), 'Unknown')
        special = ui_mappings['special'].get(int(row['special_conditions_at_site']), 'Unknown')
        
        clean_date = pd.to_datetime(row['date']).strftime('%d %b %Y')

        # Build the Popup HTML
        popup_text = f"""
        <div style="font-family: Arial; font-size: 13px; width: 230px;">
            <h4 style="margin:0 0 10px 0; color: #e74c3c; border-bottom: 1px solid #ccc;">{sev} Incident</h4>
            <b>Date:</b> {clean_date}<br>
            <b>Location:</b> {area} Area<br>
            <b>Road Type:</b> {road}<br>
            <hr style="margin: 8px 0;">
            <b>Conditions:</b><br>
            ☀️ {weather}<br>
            💡 {light}<br>
            🛣️ {surface} Surface<br>
            ⚠️ {special}<br>
            <hr style="margin: 8px 0;">
            <b>Involved:</b> {row['number_of_vehicles']} Vehicles<br>
            <b>Casualties:</b> {casualty_summary} 👤<br>
            <b>Vehicle:</b> {vehicle_summary} 🚗<br>
        </div>
        """
        
        color = get_marker_color(row['collision_severity'])

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=400),
            tooltip="Click for details"
        ).add_to(marker_cluster)

    return m