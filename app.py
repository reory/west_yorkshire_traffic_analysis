# Main streamlit script.
import sys
import os
# 1. PATH FIX: Tell Python to look one folder up for the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from src.load_data import load_wy_data, load_linked_data
from src.mappings import ui_mappings
from filters import apply_filters
from map_utils import render_incident_map
import sidebars

def reset_all_filters():
    # Only clear if there is actually something in memory.
    if st.session_state:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Add the button at the top of the sidebar
if st.sidebar.button('🔃 Reset All Filters'):
    reset_all_filters()

# --- PAGE SETUP ---
st.set_page_config(page_title='West Yorkshire Traffic Analysis', layout='wide')

@st.cache_data
def get_data():
    return load_wy_data('data/accidents.csv')

@st.cache_data
def get_linked_assets(ids):
    # Ensure paths are relative to the project root
    veh = load_linked_data('data/vehicles.csv', ids)
    cas = load_linked_data("data/casualties.csv", ids)
    print("--- Casualty Columns ---")
    print(cas.columns.tolist())
    return veh, cas

df = get_data()

filters = sidebars.render_sidebar(df, ui_mappings)

# Filters dict from sidebars.py
selected_year = filters['year']
severity_choice = filters['severity']
selected_genders = filters['genders']
weather_choice = filters['weather']
show_blackspots = filters['show_blackspots']

# --- DATA PROCESSING ---
# 1. Get initial data for the year
filtered_df = df[df['year'] == selected_year].copy()
target_ids = filtered_df['collision_index']
veh_df, cas_df = get_linked_assets(target_ids)
#-----------------------------------------------------------------------
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
#---------------------------------------------------------------
# --- MAIN DASHBOARD ---
st.title(f'West Yorkshire Traffic Analysis:🚦')
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
        top_dist = display_df['local_authority_district'].mode()[0]
        label = ui_mappings['district'].get(top_dist, 'West Yorkshire')
        st.metric('District', label)

# Row: The Map
st.subheader(f'Interactive Incident Map: {selected_year}🚦')

if display_df.empty:
    st.info("💡**Getting Started:**"
            " Please select filters from the sidebar to visualize data.")
else:

 # Call the Artist (from map_utils.py)
 m = render_incident_map(display_df, cas_df, veh_df, show_blackspots,ui_mappings)
 st_folium(m, width=1400, height=700, returned_objects=[])

# Row: Metrics
st.write('### 📊 Snapshot of the Involved Incidents')
if not display_df.empty:
    final_ids = display_df['collision_index']
    v_count = len(veh_df[veh_df['collision_index'].isin(final_ids)])
    c_count = len(cas_df[cas_df['collision_index'].isin(final_ids)])
    
    c1, c2 = st.columns(2)
    c1.metric('Total Vehicles', v_count)
    c2.metric('Total Casualties', c_count)