import streamlit as st
import pandas as pd

def apply_filters(df, cas_df, weather_choice, severity_choice, light_choice, 
                  surface_choice, road_type_choice, age_choice, 
                  selected_genders, ui_mappings):
    filtered_df = df.copy()
    
    # Severity
    if severity_choice:
        inv_sev = {v: k for k, v in ui_mappings['severity'].items()}
        target_sev = [inv_sev[s] for s in severity_choice]
        filtered_df = filtered_df[filtered_df['collision_severity'].isin(target_sev)]

    # Gender (The Refined Fix)
    if selected_genders:
        inv_gender = {v: k for k, v in ui_mappings['gender'].items()}
        target_genders = [inv_gender[g] for g in selected_genders]
        
        # Identify collision indices that have at least one of the selected genders
        mask = cas_df['sex_of_casualty'].isin(target_genders)
        valid_indices = cas_df[mask]['collision_index'].unique()
        
        filtered_df = filtered_df[filtered_df['collision_index'].isin(valid_indices)]

    # Age band - casulty based filter
    if age_choice:
        inv_age = {v: k for k, v in ui_mappings['age_choice'].items()}
        target_ages =[inv_age[a] for a in age_choice]

        # Find all collision IDs in the casualty file that match these ages.
        mask = cas_df['age_band_of_casualty'].isin(target_ages)
        valid_indices = cas_df[mask]['collision_index'].unique()

        # Filter the main dataframe to only show those accidents
        filtered_df = filtered_df[filtered_df['collision_index'].isin(valid_indices)] 

    #  Weather
    if weather_choice:
        inv_weather = {v: k for k, v in ui_mappings['weather'].items()}
        target_w = [inv_weather[w] for w in weather_choice]
        filtered_df = filtered_df[filtered_df['weather_conditions'].isin(target_w)]

    # Light Conditions
    if light_choice:
       inv_light = {v: k for k, v in ui_mappings['light'].items()}
       target_l = [inv_light[l] for l in light_choice]
       filtered_df = filtered_df[filtered_df['light_conditions'].isin(target_l)]

    # Road Surface
    if surface_choice:
        inv_surf = {v: k for k, v in ui_mappings['surface'].items()}
        target_s = [inv_surf[s] for s in surface_choice]
        filtered_df = filtered_df[filtered_df['road_surface_conditions'].isin(target_s)]

    # Road Type - Using the text-based column (Index 49) from mappings.py
    if road_type_choice:
        # Since the sidebar choice IS the text, we check it directly 
        # against the 'display_road_type' column.
        col_name = 'display_road_type'
        
        if col_name in filtered_df.columns:
            # We filter for the exact strings selected in the sidebar
            filtered_df = filtered_df[filtered_df[col_name].isin(road_type_choice)]
            # Force both to lowercase to ignore spelling/case mistakes
            filtered_df = filtered_df[
                filtered_df[col_name].str.lower().isin([x.lower() for x in road_type_choice])]
        else:
            # Emergency fallback to column 20 if 49 isn't available
            inv_road = {v: k for k, v in ui_mappings['road_type'].items()}
            target_r = [inv_road[r] for r in road_type_choice]
            filtered_df = filtered_df[filtered_df['road_type'].astype(float).astype(int).isin(target_r)]

    return filtered_df