from fpdf import FPDF
from datetime import datetime
import os

now = datetime.now()
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

class WYTrafficReport(FPDF):
    """Generate a traffic report with all the findings."""

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "West Yorkshire Traffic Analysis Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_pdf_report(summary_data, hotspots_list=None, chart_folder="output_charts"):

    pdf = WYTrafficReport()
    pdf.set_auto_page_break(auto=True)

    # Incident summary.
    pdf.add_page()

    # Add a logo with adjustments for sizes.
    pdf.image("assets/logo.png", x=10, y=10, w=50)

    # Add the timestamp so user can see when PDF was created.
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0,3, f"Generated document on: {timestamp}", ln=1, align="R")

    # pushes the page down from the top.
    pdf.ln(20) 

    # The main header.
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 6, "Traffic Incident Summary", ln=1, align="L")
    # Add space between Header and the Summary data.
    pdf.ln(10)
    
    # Loop through the terminal prints and put them on the pdf report.
    pdf.set_font("Arial", "", 11)
    # Increase or decrease line height.
    line_h = 12

    for line in summary_data:
        # Clean the line of any invisible or weird characters.
        clean_line = str(line).strip()
        # If line is empty add a small vertical space.
        if not clean_line:
            pdf.ln(line_h / 2)
        else:
            if ":" in clean_line and not clean_line.startswith(" -"):
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, line_h, clean_line, ln=1, align="L")
                pdf.set_font("Arial", "", 11)
            else:
                # Use a defined width - to avoid space errors in the PDF.
                pdf.cell(0, line_h, clean_line, ln=1, align="L")

    if hotspots_list:
        pdf.add_page()
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Top 5 Priority Accident Blackspots", ln=1, align="L")
        pdf.set_font("Arial", "", 11)

        for spot in hotspots_list:

            lat = spot['latitude']
            lon = spot['longitude']
            # The Google maps URL
            map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            # Use the area and road_type we got from reverse_geocoder.
            text = f"- {spot['site_label']} | {spot['road_type']} ({spot['count']} incidents)"
            
            # Make the link look clickable.
            pdf.set_text_color(0, 0, 255) # Blue text
            pdf.set_font("Arial", "U", 11) # Underlined

            # The link parameter makes the whole line a clickable button.
            pdf.cell(0, 8, text, ln=1, align="L", link=map_url)

        # Resst back to black text/normal font for the rest of the PDF.
        pdf.set_text_color(0, 0, 0) # Black
        pdf.set_font("Arial", "", 11)

        special_chart = "blackspot_priority_analysis.png"
        special_chart_path = os.path.join(chart_folder, special_chart)

        if os.path.exists(special_chart_path):
            pdf.ln(10)
            pdf.image(special_chart_path, x=10, w=190)
        else:
            print(f"Warning: Could not find {special_chart}")
    
    # Charts Visuals- use sorted() so they appear in a consistent order.
    charts = sorted([c for c in os.listdir(chart_folder)if c.endswith(".png")])
    
    # For loop to skip the chart that already has been printed earlier.
    for i, chart_name in enumerate(charts):
        if "blackspot_priority_analysis" in chart_name.lower():
            print(f"Skipping duplicate: {chart_name}")
            continue

        if i % 1 == 0:
            pdf.add_page()
        else:
            pdf.ln(2)

        chart_path = os.path.join(chart_folder, chart_name)

        # Clean up the name for the chart caption (eg, remove underscores, etc)
        caption = chart_name.replace("_", " ").replace(".png", "").title()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 1, caption, ln=1, align="C")
        # Manual gap between charts.
        pdf.ln(20)
        pdf.image(chart_path, x=20, w=170)

    target_folder = "output_charts"
    filename = "West_Yorkshire_Traffic_Analysis_Report.pdf"

    full_path = os.path.join(target_folder, filename)

    pdf.output(full_path)
    print(f"PDF REPORT GENERATED: {full_path}")