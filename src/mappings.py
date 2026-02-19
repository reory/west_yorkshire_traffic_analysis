# Dictionary for serverity by district.
district_names = {
    "E08000035": "Leeds",
    "E08000032": "Bradford",
    "E08000036": "Wakefield",
    "E08000034": "Calderdale",
    "E08000033": "Kirklees"
}

# Map numeric severity codes to readable labels.
severity_labels = {
    1: "Fatal",
    2: "Serious",
    3: "Slight"
}

# Map numeric weather codes to readable labels.
weather_labels = {
    1: "Fine (no high winds)",
    2: "Raining (no high winds)",
    3: "Snowing (no high winds)",
    4: "Fine (high winds)",
    5: "Raining (high winds)",
    6: "Snowing (high winds)",
    7: "Fog or Mist",
    8: "Other",
    9: "Unknown" 
}
# Map numeric road class to readable labels.
road_class_labels = {
    1: "Motorway", 
    2: "A/(M)", 
    3: "A", 
    4: "B", 
    5: "C", 
    6: "Unclassified"
}

# Map numeric road types to readable labels
road_type_labels = {
    1: "Roundabout",
    2: "One way",
    3: "Dual carriageway",
    6: "Single carriageway",
    7: "Slip",
    9: "Unknown",
    12: "One way(alt)",
    15: "Other"
}

# Map the numeric codes.
light_labels = {
    1: "Daylight",
    4: "Darkness (street lights lit)",
    5: "Darkness (no street lights)",
    6: "Darkness (street lights unlit)",
    7: "Darkness (unknown lighting)",
    8: "Twilight",
    9: "Unknown"
}

surface_labels = {
    1: "Dry",
    2: "Wet / Damp",
    3: "Snow",
    4: "Frost / Ice",
    5: "Flood",
    6: "Oil",
    7: "Mud",
    9: "Unknown"
}

special_labels = {
    -1: "No special conditions",
    0: "No special conditions",
    1: "Auto traffic signal out",
    2: "Auto signal partially defective",
    3: "Permanent road signing defective",
    4: "Roadworks",
    5: "Road surface defective",
    6: "Oil or diesel",
    7: "Mud",
    8: "Road layout altered (temporary)",
    9: "Unknown"
}

urban_rural_labels = { 
    1: "Urban", 
    2: "Rural" 
}

gender_options = {
    1: 'Male', 
    2: 'Female',
    9: 'Unknown',
}

age_band_labels = {
    1: "0-5", 2: "6-10", 3: "11-15", 4: "16-20", 5: "21-25",
    6: "26-35", 7: "36-45", 8: "46-55", 9: "56-65", 10: "66-75", 
    11: "Over 75"
}

casualty_class_labels = {
    1: "Driver/Rider", 
    2: "Passenger", 
    3: "Pedestrian"
}
# The Master Bundle
ui_mappings = {
    'severity': severity_labels,
    'light': light_labels,
    'surface': surface_labels,
    'special': special_labels,
    'weather': weather_labels,
    'road_type': road_type_labels,
    'area': urban_rural_labels,
    'district': district_names,
    'gender': gender_options,
    'age_choice': age_band_labels
}