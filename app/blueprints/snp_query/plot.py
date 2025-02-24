from flask import Blueprint, request, jsonify, render_template, session
import plotly.express as px
import pandas as pd

try:
    # absolute import version
    from app.blueprints.snp_query.views import snp_bp
    from app.blueprints.db_api.db_api import db
except ImportError:
    # relative import version
    from views import snp_bp
    from ..db_api.db_api import db


plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/plot-fst', methods=['POST'])
def plot_fst():
    try:
        # Retrieve SNP IDs and selected populations from the form submission
        fst_data = session.get('fst_data')
        snp_ids = session.get('snp_ids')
        selected_populations = session.get('selected_populations')

        # Debugging statements to check the inputs
        print(f"Received SNP IDs: {snp_ids}")
        print(f"Received selected populations: {selected_populations}")

        # Check if populations and SNPs are selected
        if not snp_ids or not selected_populations:
            print("No SNP IDs or populations selected.")
            return jsonify({"message": "No plot available"}), 400

        # If no valid FST data is available, return a message
        if all(fst_value == 'N/A' for population in fst_data for fst_value in fst_data[population].values()):
            print("All FST values are 'N/A'. No valid data available.")
            return jsonify({"message": "No plot available"}), 400

        # Prepare data for plotting: Convert FST data into a Pandas DataFrame
        plot_data = []
        for population in selected_populations:
            for snp_id in snp_ids:
                fst_value = fst_data[population].get(snp_id, 'N/A')
                if fst_value != 'N/A':
                    plot_data.append({
                        'SNP ID': snp_id,
                        'Population': population,
                        'FST': fst_value
                    })
                    print(f"Adding data for SNP {snp_id}, Population {population}, FST {fst_value}")

        df = pd.DataFrame(plot_data)
        print(f"DataFrame created: {df}")

        # If no valid data available after processing, show "No plot available" message
        if df.empty:
            print("DataFrame is empty. No valid data for plotting.")
            return jsonify({"message": "No plot available"}), 400

        # Generate the interactive grouped bar plot using Plotly
        print("Generating Plotly bar plot...")
        fig = px.bar(df, x="SNP ID", y="FST", color="Population", barmode="group",
                     labels={"FST": "FST Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="FST Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="FST Value")

        # Convert the Plotly figure to HTML for embedding
        plot_html = fig.to_html(full_html=False)
        print("Plot generated successfully.")

        return plot_html

    except Exception as e:
        # Handle any potential error gracefully
        print(f"Error generating plot: {str(e)}")
        return jsonify({"message": "Error generating plot. Please try again later."}), 500