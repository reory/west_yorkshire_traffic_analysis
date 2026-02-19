import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import os

#print(silence debugging prints, turn on when ready)

# Create an Output chart folder if it does not exist.
if not os.path.exists("output_charts"):
    os.makedirs("output_charts")

# The Academic Grayscale Look for all the charts.
plt.style.use('grayscale')

def bar_chart(series, title, xlabel, ylabel, color=None):
    plt.figure(figsize=(12, 16))
    series.plot(kind="bar", color=color)
    plt.title(title, fontsize=18)
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    
    # Save charts insted of plt.show(). plt.show() causes weird behaviour.
    clean_title = title.replace(" ", "_").replace("(", "").replace(")", "") + ".png"
    filename = f"{clean_title}"
    save_path = os.path.join("output_charts", filename)
    plt.savefig(save_path)
    # Important closes the plot memory so the script keeps moving.
    plt.close()
    #print(f"Chart saved: {save_path}")

def stacked_bar_chart(df_comparison, title, xlabel, ylabel, colors):
    # This uses your master height of 16
    plt.figure(figsize=(12, 16))
    df_comparison.plot(kind="bar", stacked=True, color=colors, ax=plt.gca())
    plt.title(title)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=0)
    plt.yticks(fontsize=12)
    plt.legend(title="Severity")
    plt.tight_layout()
    
    clean_title = title.replace(" ", "_") + ".png"
    plt.savefig(f"output_charts/{clean_title}")
    plt.close()


def pie_chart(series, title, colors=None, pctdistance=1.0, labeldistance=1.05):
    plt.figure(figsize=(12, 16))

    #Label styling.
    label_font = {
        'fontsize': 14,
        'color': 'black'
    }
    series.plot(
        kind="pie",
        autopct="%1.1f%%", 
        startangle=90, 
        colors=colors,
        pctdistance=pctdistance,
        labeldistance=labeldistance,
        textprops=label_font
    )
    plt.title(title, pad=20, fontsize=16)
    plt.ylabel("") # hides the y axis.
    plt.tight_layout()
    
    # Save charts insted of plt.show(). plt.show() causes weird behaviour.

    clean_title = title.replace(" ", "_").replace("(", "").replace(")", "") + ".png"
    filename = f"{clean_title}"
    save_path = os.path.join("output_charts", filename)
    plt.savefig(save_path)
    # Important closes the plot memory so the script keeps moving.
    plt.close()
    #print(f"Chart saved: {save_path}")

def generate_blackspots_chart(df, 
                              chart_folder, 
                              hotspots_data=None, data_duration="unknown"):
    """Generate the accident blackspots chart for west yorkshire."""
    
    # If no data passed, chart cant be drawn.
    if not hotspots_data:
        print(" No hotspots data provided for chart.")
        return
    
    labels = []
    top_counts = []

    for spot in hotspots_data:
        
        # We use 'site_label' which contains the coordinates + area name
        area = spot['area'] 
        road_context = spot['road_type']
        count = spot['count']
        
        # Cleanly formatted: Coordinates (Area) \n Road Type
        full_label = f"{area}\n({road_context})"

        labels.append(full_label)
        top_counts.append(count)

    # --- Chart Drawing Logic ---
    plt.figure(figsize=(12, 10))
    y_pos = np.arange(len(labels))
    
    # Reverse the lists so the highest count is at the top
    bars = plt.barh(y_pos, top_counts[::-1], color="#F70202", 
                    align="center", height=0.6)
    plt.yticks(y_pos, labels[::-1], fontsize=11)
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{int(width)} Incidents', va='center', color='black', fontsize=12)
        
    plt.title("Priority Analysis: Top 5 West Yorkshire Blackspots", 
              fontsize=18, pad=25, weight='bold')
    plt.xlabel("Total Incident Count", fontsize=12)
    plt.xlim(0, max(top_counts) * 1.4) 
    plt.tight_layout(pad=3.0)
    
    # Add a note for the user to open the PDF for a full summary.
    plt.figtext(
        0.5, 
        0.01, f"Anaylsis Period: {data_duration} | Coordinates listed in full report.",
        ha="center",
        fontsize=12,
        style="italic",
        color='black'
        )
    
    # Save PDF.
    save_path = os.path.join(chart_folder, "blackspot_priority_analysis.png")
    plt.savefig(save_path, dpi=300)
    plt.close()