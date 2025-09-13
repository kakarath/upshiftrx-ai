# Graphs are natural for drug ↔ disease ↔ paper connections. Using NetworkX

import argparse
import os
import glob
import pandas as pd
import networkx as nx
from pyvis.network import Network
from pathlib import Path

def build_graph(input_file, output_file="results/drug_disease_graph.html"):
    # Validate and sanitize file paths
    input_path = Path(input_file).resolve()
    output_path = Path(output_file).resolve()
    
    # Load dataset with error handling
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Input file is empty: {input_path}")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    if df.empty:
        raise ValueError("Dataset is empty")

    # Ensure required cols
    required_cols = {"drug", "disease"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Expected columns {required_cols}, got {df.columns}")

    # Aggregate counts
    grouped = (
        df.groupby(["drug", "disease"])
          .size()
          .reset_index(name="count")
    )

    max_count = grouped["count"].max()

    # Init PyVis network
    net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333", notebook=False)
    net.barnes_hut()

    # Add nodes + edges (avoid duplicates)
    added_nodes = set()
    for _, row in grouped.iterrows():
        drug = str(row["drug"])
        disease = str(row["disease"])
        count = int(row["count"])

        if drug not in added_nodes:
            net.add_node(drug, label=drug, color="#1976d2", shape="dot", size=20)
            added_nodes.add(drug)
        if disease not in added_nodes:
            net.add_node(disease, label=disease, color="#d32f2f", shape="dot", size=20)
            added_nodes.add(disease)
        net.add_edge(drug, disease, value=count, title=f"{count} papers")

    # Enable search/filter
    net.show_buttons(filter_=['nodes'])

    # Save initial HTML with error handling
    try:
        os.makedirs(output_path.parent, exist_ok=True)
        net.save_graph(str(output_path))
    except PermissionError:
        raise PermissionError(f"Permission denied writing to: {output_path}")
    except Exception as e:
        raise IOError(f"Error saving graph: {e}")

    # Inject slider with dynamic max
    slider_html = f"""
    <div style="position:absolute; top:10px; left:10px; background:#fff; padding:10px; border:1px solid #ccc; border-radius:8px; z-index:9999;">
        <label for="edgeSlider"><b>Min #papers:</b></label>
        <input type="range" id="edgeSlider" min="1" max="{max_count}" value="1" step="1" 
               oninput="document.getElementById('sliderValue').innerText=this.value">
        <span id="sliderValue">1</span>
    </div>
    """ + """
    <script type="text/javascript">
        const slider = document.getElementById("edgeSlider");
        slider.addEventListener("input", function() {
            const minVal = parseInt(this.value);
            network.body.data.edges.forEach(function(edge) {
                if (edge.value < minVal) {
                    edge.hidden = true;
                } else {
                    edge.hidden = false;
                }
            });
            network.redraw();
        });
    </script>
    """

    # Read back HTML and patch with error handling
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("</body>", slider_html + "\n</body>")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        raise IOError(f"Error updating HTML file: {e}")

    print(f"Graph saved to {output_path} with interactive slider (max={max_count})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a drug–disease graph")
    parser.add_argument(
        "--input",
        type=str,
        default="results/examples/sample_results.csv",
        help="Path to CSV file (default: results/examples/sample_results.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/drug_disease_graph.html",
        help="Output HTML file"
    )
    args = parser.parse_args()

    build_graph(args.input, output_file=args.output)
