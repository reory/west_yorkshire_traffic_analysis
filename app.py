"""Main streamlit script"""

import streamlit as st
from streamlit_folium import st_folium

from src.analysis.report_service import build_report
from src.data_sources import DATA_SOURCES
from src.filters import apply_filters
from src.load_data import (
    get_data_period,
    load_collision_years,
    load_linked_data,
)
from src.map_utils import render_incident_map
from src.mappings import ui_mappings
from src.sidebars import render_sidebar

# --- PAGE SETUP ---
st.set_page_config(page_title='West Yorkshire Traffic Analysis', layout='wide')


def reset_all_filters():
    """Clear all keys from Streamlit session state and rerun the app."""

    # Only clear if there is actually something in memory.
    if st.session_state:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Add the button at the top of the sidebar
if st.sidebar.button('🔃 Reset All Filters'):
    reset_all_filters()


@st.cache_data
def get_data():
    """Load all configured collision datasets."""

    return load_collision_years()


@st.cache_data
def get_linked_assets(year, ids):
    """Load linked vehicle and casualty data for the selected year."""

    source = DATA_SOURCES[year]

    # Ensure paths are relative to the project root
    veh = load_linked_data(source["vehicles"], ids)
    cas = load_linked_data(source["casualties"], ids)
    #print("--- Casualty Columns ---")
    #print(cas.columns.tolist())
    return veh, cas

df = get_data()

filters = render_sidebar(df, ui_mappings)

# Filters dict from sidebars.py
selected_year = filters['year']
severity_choice = filters['severity']
selected_genders = filters['genders']
weather_choice = filters['weather']
show_markers = filters['show_markers']
show_heatmap = filters['show_heatmap']

# --- DATA PROCESSING ---
# 1. Get initial data for the year
filtered_df = df[df['year'] == selected_year].copy()

target_ids = filtered_df['collision_index']

veh_df, cas_df = get_linked_assets(
    selected_year, 
    target_ids.tolist(),
)

# 2. Apply complex filters (from filters.py)
filtered_df = apply_filters(
    df=filtered_df, 
    cas_df=cas_df, 
    weather_choice=filters['weather'],
    severity_choice=filters['severity'],
    light_choice=filters['light'],
    surface_choice=filters['surface'],
    road_type_choice=filters['road_type'],
    age_choice=filters['age_choice'],
    selected_genders=filters['genders'],
    ui_mappings=ui_mappings
)

# 3. Handle Empty State
active_filters = [
    severity_choice,
    selected_genders,
    weather_choice,
    filters['age_choice'],
    filters['light'],
    filters['surface'],
    filters['road_type']
]
# If every single list in active_filters is empty show none. 
# otherwise show results.
if not any(active_filters):
    display_df = filtered_df.iloc[0:0]
else:
    display_df = filtered_df

# Main Dashboard -------------------------------------------------
st.title('West Yorkshire Traffic Analysis:🚦')
st.subheader(f'Insights and Hotspots for {selected_year}')
st.markdown('---')

# Row: Key statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Accidents', len(display_df))
with col2:
    if not display_df.empty:
        raw_mode = display_df['collision_severity'].mode()[0]
        label = ui_mappings['severity'].get(raw_mode, 'Unknown')
        st.metric('Most Common Severity', label)
    else:
        st.metric('Most Common Severity', 'N/A')
with col3:
    if not display_df.empty:
        top_dist = display_df['local_authority_ons_district'].mode()[0]
        label = ui_mappings['district'].get(top_dist, 'West Yorkshire')
        st.metric('District', label)

# Row: The Map--------------------------------------------------------
st.subheader(f'Interactive Incident Map: {selected_year}🚦')

if display_df.empty:
    st.info("💡**Getting Started:**"
            " Please select filters from the sidebar to visualise data.")
else:

 # Call the Artist (from map_utils.py)
 m = render_incident_map(
    display_df, 
    cas_df, 
    veh_df,
    show_markers, 
    show_heatmap,
    ui_mappings
)
 st_folium(m, width=1400, height=700, returned_objects=[])

# Row: Metrics--------------------------------------------------------
st.write('### 📊 Snapshot of the Involved Incidents')
if not display_df.empty:
    final_ids = display_df['collision_index']
    v_count = len(veh_df[veh_df['collision_index'].isin(final_ids)])
    c_count = len(cas_df[cas_df['collision_index'].isin(final_ids)])
    
    c1, c2 = st.columns(2)
    c1.metric('Total Vehicles', v_count)
    c2.metric('Total Casualties', c_count)

# PDF Report Generation----------------------------------------------
st.markdown("---")
st.subheader("📝 Download Report")

if not display_df.empty and st.button("📝 Generate PDF report"):

    with st.spinner("Building Report...please wait!"):
        duration = get_data_period(display_df)
        
        report_ids = display_df["collision_index"]

        report_vehicles_df = veh_df[
            veh_df["collision_index"].isin(report_ids)
        ].copy()

        report_casualties_df = cas_df[
            cas_df["collision_index"].isin(report_ids)
        ].copy()

        # Build Filtered PDF Report
        pdf_path = build_report(
            display_df,
            report_vehicles_df,
            report_casualties_df,
            duration,
            chart_folder="temp_report",
        )

    with open(pdf_path, "rb") as pdf_file:

        # PDF Download Button
        st.download_button(
            label="⬇️ Download PDF report",
            data=pdf_file.read(),
            file_name="West_Yorkshire_Traffic_Analysis_Report.pdf",
            mime="application/pdf"
        )