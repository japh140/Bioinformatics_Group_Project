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
                    
        df = pd.DataFrame(plot_data)

        # Generate the interactive grouped bar plot using Plotly
        fig = px.bar(df, x="SNP ID", y="FST", color="Population", barmode="group",
                     labels={"FST": "FST Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="FST Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="FST Value")

        # Convert the Plotly figure to HTML for embedding
        plot_html = fig.to_html(full_html=False)

        return plot_html

    except Exception as e:
        # Handle any potential error gracefully
        print(f"Error generating plot: {str(e)}")
        return jsonify({"message": "Error generating plot. Please try again later."}), 500
    


@plot_bp.route('/plot-nsl', methods=['POST'])
def plot_nsl():
    try:
        # Get SNP IDs and selected populations from the POST request
        snp_ids = session.get('snp_ids')
        selected_populations = session.get('selected_populations')

        print(f"Received SNP IDs: {snp_ids}")
        print(f"Received selected populations: {selected_populations}")

        # Retrieve nSL data from the session (placeholder values for example)
        nsl_data = session.get('nsl_data', {
            'Bengali': {'SNP_1': 1.5, 'SNP_2': 2.0},
            'Gujarati': {'SNP_1': 0.8, 'SNP_2': 1.2},
            'Punjabi': {'SNP_1': 1.1, 'SNP_2': 1.3},
            'Telugu': {'SNP_1': 2.1, 'SNP_2': 1.6}
        })
        
        print(f"nsl_data from session: {nsl_data}")

        # Prepare data for plotting
        plot_data = []
        for population in selected_populations:
            for snp_id in snp_ids:
                # Get the nSL value from the nsl_data
                nsl_value = nsl_data.get(population, {}).get(snp_id, 'N/A')
                print(f"Checking nSL value for {population}, {snp_id}: {nsl_value}")
                if nsl_value != 'N/A':  # Only add valid nSL values
                    plot_data.append({
                        'SNP ID': snp_id,
                        'Population': population,
                        'nSL': nsl_value
                    })

        # If no valid data is available, return an error message
        if not plot_data:
            return jsonify({"message": "No plot available for the selected SNPs and populations."}), 400

        # Create a DataFrame from the plot data
        df = pd.DataFrame(plot_data)

        # Generate the Plotly bar plot
        fig = px.bar(df, x="SNP ID", y="nSL", color="Population", barmode="group",
                     labels={"nSL": "nSL Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="nSL Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="nSL Value")

        # Convert the plot to HTML for embedding in the page
        plot_html = fig.to_html(full_html=False)

        # Return the plot HTML to the client for embedding in the plot container
        return plot_html

    except Exception as e:
        print(f"Error generating nSL plot: {str(e)}")
        return jsonify({"message": "Error generating nSL plot. Please try again later."}), 500