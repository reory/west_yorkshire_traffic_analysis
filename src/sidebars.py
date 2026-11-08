import streamlit as st


def render_sidebar(df, ui_mappings):
    """
    Renders all sidebar filters and returns the user's selections.
    """

    # Top: Title and Year--------------------------------------
    st.sidebar.title("🔍 Advanced Filters")

    # Year Selection
    years = sorted(df["year"].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Filter by Year", years)

    # ----------Incident Details--------------------------------
    st.sidebar.markdown("---")
    with st.sidebar.expander("🚗 Incident Details", expanded=False):
        # Multi-select filters
        severity_choice = st.multiselect(
            "Incident Severity",
            options=list(ui_mappings["severity"].values()),
            key="sev_filter",  # This wires to the refresh button in app.py.
        )
        selected_genders = st.multiselect(
            "Casualty Gender",
            options=list(ui_mappings["gender"].values()),
            key="cas_filter",
        )
        age_choice = st.multiselect(
            "Age of casualty",
            options=list(ui_mappings["age_choice"].values()),
            key="age_filter",
        )

    # ----------Environment details------------------------------
    st.sidebar.markdown("---")
    with st.sidebar.expander("🌍 Environment and Infrastructure", expanded=False):
        # Mulit-select filters.
        weather_choice = st.multiselect(
            "Weather Conditions",
            options=list(ui_mappings["weather"].values()),
            key="weather_filter",
        )
        light_choice = st.multiselect(
            "Lighting", 
            options=list(ui_mappings["light"].values()), 
            key="light_filter",
        )
        surface_choice = st.multiselect(
            "Road Surface",
            options=list(ui_mappings["surface"].values()),
            key="surface_filter",
        )
        road_type_choice = st.multiselect(
            "Road Type",
            options=list(ui_mappings["road_type"].values()),
            key="road_type_filter",
        )

    # -------------------Map Layers-------------------------------
    st.sidebar.markdown("---")
    with st.sidebar.expander("🗺️ Map Layers", expanded=False):
        show_markers = st.toggle(
            "Incident Markers",
            value=True,
        )

        show_heatmap = st.toggle(
            "Heatmap Overlay",
            value=False,
        )

    # -------------------Legends--------------------------------------
    st.sidebar.markdown("---")
    with st.sidebar.expander("🗺️ Map Legend", expanded=False):
        st.markdown(
            """<div style="font-size: 0.85rem; margin-bottom: 10px;">
            🔴 <b>Fatal</b> | 🟠 <b>Serious</b> | 🟡 <b>Slight</b></div>
                            """,
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("<div style='padding: 5px;'></div>", unsafe_allow_html=True)

    # ------------------Heatmap legend - shows if toggle is on-----------------
    if show_heatmap:
        st.markdown("---")
        st.markdown("**🔥 Heatmap Intensity**")
        st.markdown(
            """
            <div style="width: 100%; height: 10px; background: linear-gradient(to right, blue, lime, red); border-radius: 5px;"></div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem;">
                <span>Low</span><span>Medium</span><span>High</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Return everything as a dictionary
    return {
        "year": selected_year,
        "severity": severity_choice,
        "genders": selected_genders,
        "weather": weather_choice,
        "show_markers": show_markers,
        "show_heatmap": show_heatmap,
        "light": light_choice,
        "surface": surface_choice,
        "road_type": road_type_choice,
        "age_choice": age_choice,
    }
