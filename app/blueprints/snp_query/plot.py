from flask import Blueprint, request, jsonify, session
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
        # Retrieve snp_ids and combined_data from the session
        snp_ids = session.get('snp_ids')
        combined_data = session.get('stats_data')

        # Retrieve selected_populations from the request JSON payload
        request_data = request.get_json()
        selected_populations = request_data.get('selected_populations')     

        # Check if populations and SNPs are selected
        if not snp_ids or not selected_populations:
            return jsonify({"message": "No plot available"}), 400

        # If no valid FST data is available, return a message
        if all(combined_data[population][snp_id]['fst'] == 'N/A' for population in selected_populations for snp_id in snp_ids):
            return jsonify({"message": "No plot available"}), 400

        # Prepare data for plotting
        plot_data = []
        for population in selected_populations:
            for snp_id in snp_ids:
                fst_value = combined_data[population].get(snp_id, {}).get('fst', 'N/A')
                if fst_value != 'N/A':
                    plot_data.append({
                        'SNP ID': snp_id,
                        'Population': population,
                        'FST': fst_value
                    })

        # Create a Pandas DataFrame from the plot data
        df = pd.DataFrame(plot_data)

        # Generate the interactive grouped bar plot using Plotly
        fig = px.bar(df, x="SNP ID", y="FST", color="Population", barmode="group",
                     labels={"FST": "FST Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="FST Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="FST Value")

        fig.add_hline(y=0.15, line_dash="dash", line_color="black")

        # Convert the Plotly figure to HTML for embedding
        plot_html = fig.to_html(full_html=False)

        return plot_html

    except Exception as e:
        return jsonify({"message": "Error generating plot. Please try again later."}), 500


@plot_bp.route('/plot-nsl', methods=['POST'])
def plot_nsl():
    try:
        # Retrieve snp_ids adn combined_data from the session
        snp_ids = session.get('snp_ids')
        combined_data = session.get('stats_data')

        # Retrieve selected_populations from the request JSON payload
        request_data = request.get_json()
        selected_populations = request_data.get('selected_populations')

        # Check if populations and SNPs are selected
        if not snp_ids or not selected_populations:
            return jsonify({"message": "No plot available"}), 400

        # If no valid nSL data is available, return a message
        if all(combined_data[population][snp_id]['nsl'] == 'N/A' for population in selected_populations for snp_id in snp_ids):
            return jsonify({"message": "No plot available"}), 400

        # Prepare data for plotting: Convert nSL data into a Pandas DataFrame
        plot_data = []
        for population in selected_populations:
            for snp_id in snp_ids:
                nsl_value = combined_data[population].get(snp_id, {}).get('nsl', 'N/A')
                if nsl_value != 'N/A':
                    plot_data.append({
                        'SNP ID': snp_id,
                        'Population': population,
                        'nSL': nsl_value
                    })

        # Create a Pandas DataFrame from the plot data
        df = pd.DataFrame(plot_data)

        # Generate the interactive grouped bar plot using Plotly
        fig = px.bar(df, x="SNP ID", y="nSL", color="Population", barmode="group",
                     labels={"nSL": "nSL Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="nSL Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="nSL Value")

        fig.add_hline(y=2, line_dash="dash", line_color="black")
        fig.add_hline(y=-2, line_dash="dash", line_color="black")

        # Convert the Plotly figure to HTML for embedding
        plot_html = fig.to_html(full_html=False)

        return plot_html

    except Exception as e:
        return jsonify({"message": "Error generating nSL plot. Please try again later."}), 500
