# West Yorkshire Traffic Safety Intelligence 🚗📊

### [🚀 View Live Dashboard](https://share.streamlit.io/reory/west_yorkshire_traffic_analysis/main/app.py) 

## 📖 Project Overview
An interactive geographic intelligence dashboard analyzing **2024 STATS19 traffic safety data** specifically for the West Yorkshire region. This tool visualizes over 1,600 incidents, providing local authorities and researchers with the ability to filter by severity, road conditions, and casualty demographics to identify high-risk hotspots.

## 📈 Visual Analytics & Reporting
Beyond the interactive map, this project includes a deep-dive statistical analysis:
* **Forensic Charts:** Time-series analysis and vehicle-type distributions (available in the `output_charts/` folder).
* **Final Report:** A comprehensive PDF summary of findings, including identifying the most frequent vehicle involvements (e.g., VW Golf) and fatal incident profiles.

> **Note:** The data has been optimized and "trimmed" from the national UK dataset to focus exclusively on West Yorkshire, reducing file size by 90% for lightning-fast performance.

## 🛠️ Tech Stack
* **Python / Streamlit:** Web interface and interactivity.
* **Pandas / NumPy:** High-speed data filtering and cleaning.
* **Folium:** Geospatial mapping and cluster visualization.
* **Matplotlib:** Static chart generation for reporting.

## 📂 Project Structure
* `app.py`: The live web application.
* `data/`: Processed West Yorkshire CSV files.
* `output_charts/`: PNG exports of incident trends.
* `src/`: Backend logic for data processing and mappings.
* `West_Yorkshire_Report.pdf`: The final analytical summary.


## 🚀 Installation & Local Use
1. Clone: `git clone https://github.com/reory`
2. Install: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

## 🙏 Acknowledgments & Thanks

A huge thank you to:
* **Department for Transport (DfT):** For providing the open-source road safety data that makes this analysis possible.
* **The Streamlit Community:** For the incredible tools and support that help bring data to life.
* **West Yorkshire Authorities:** For their ongoing work in improving road safety across our region.

Special thanks to my family for their "rigorous" bug testing and support during the late-night coding sessions! 🍻

**Developed by:** Roy Peters | Leeds, UK
