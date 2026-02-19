# 🚦 West Yorkshire Traffic Analysis & Forensic Reporting

An interactive intelligence dashboard and automated reporting tool built to analyze road safety data across West Yorkshire. This project transforms raw government datasets into actionable insights using a modern Python stack.

## 🚀 Live Demo
**Check out the live dashboard here:** [https://westyorkshiretrafficanalysis-s4uloec7gumf65rz2thpl3.streamlit.app/]

---

## 🛠️ Project Architecture
This project is divided into two main components to balance real-time interaction with deep-dive analysis:

### 1. Interactive Dashboard (`app.py`)
The "Frontend" of the project. It provides a real-time interface for users to explore the data.
* **Dynamic Geospatial Mapping:** Visualizes accident hotspots across Leeds, Bradford, Wakefield, Kirklees, and Calderdale.
* **Instant Filtering:** Filter by Severity (Fatal, Serious, Slight), Year, Weather, and Road Type.
* **Key Metrics:** High-level KPIs that update instantly based on user selection.

### 2. Forensic Reporting Engine (`main.py`)
The "Analytical Backend." This script handles the heavy lifting of data visualization and document generation.
* **16 Custom Charts:** Generates a comprehensive suite of visualizations (Trend lines, Hourly heatmaps, Vehicle type distributions).
* **Automated PDF Generation:** Compiles all 16 charts into a professional forensic report (`West_Yorkshire_Report.pdf`) for offline review.

---

## 📁 File Structure
* **`app.py`**: Entry point for the Streamlit web application.
* **`main.py`**: Logic for chart generation and PDF reporting.
* **`src/`**: Modularized helper scripts (`load_data.py`, `filters.py`, `map_utils.py`).
* **`data/`**: Regionalized West Yorkshire datasets (Accidents, Vehicles, Casualties).
* **`reports/`**: Destination folder for generated PDF forensic analyses.

---

## 🧰 Tech Stack
* **Python 3.10** (Development Environment)
* **Streamlit**: For the web interface.
* **Pandas**: For high-performance data manipulation.
* **Folium/Leaflet**: For interactive geospatial mapping.
* **Matplotlib/Seaborn**: For forensic chart generation.
* **FPDF/ReportLab**: For automated PDF document creation.
* **reverse-geocoder**: For high-speed, offline reverse geocoding of incident coordinates into                           human-readable locations.

---

## ⚙️ Installation & Local Usage
To run this project locally:
1. Clone the repo: `git clone https://github.com/reory/west_yorkshire_traffic_analysis.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the app: `streamlit run app.py`

---

## 🙏 Acknowledgments
* **Data Source:** UK Department for Transport (DfT) Open Data.
* **Community:** Thanks to the Streamlit and Python communities for the robust library support.
* **Testing:** Special thanks to my family for "Quality Assurance" and bug reporting! 🍻

---

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
