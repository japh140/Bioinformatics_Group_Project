from flask import Blueprint, request, jsonify, session
import plotly.express as px
import pandas as pd

try:
    # absolute import version
    from app.blueprints.snp_query.views import snp_bp
except ImportError:
    # relative import version
    from views import snp_bp


plot_bp = Blueprint('plot', __name__)

@plot_bp.route('/plot-fst', methods=['POST'])
def plot_fst():
    try:
        # retrieve stats data and snp list from session (population-comparison route)
        snp_ids = session.get('snp_ids')
        combined_data = session.get('stats_data')

        # retrive population list from population comparison template 
        request_data = request.get_json()
        selected_populations = request_data.get('selected_populations')     

        if not snp_ids or not selected_populations:
            return jsonify({"message": "No plot available"}), 400

        if all(combined_data[population][snp_id]['fst'] == 'N/A' for population in selected_populations for snp_id in snp_ids):
            return jsonify({"message": "No plot available"}), 400

        # get fst data from combined_data 
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

        df = pd.DataFrame(plot_data)

        # bar chart 
        fig = px.bar(df, x="SNP ID", y="FST", color="Population", barmode="group",
                     labels={"FST": "FST Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="FST Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="FST Value")

        fig.add_hline(y=0.15, line_dash="dash", line_color="black")

        # convert the bar chart to HTML for embedding
        plot_html = fig.to_html(full_html=False)

        return plot_html

    except Exception as e:
        return jsonify({"message": "Error generating plot. Please try again later."}), 500


@plot_bp.route('/plot-nsl', methods=['POST'])
def plot_nsl():
    try:
        # retrieve stats data and snp list from session (population-comparison route)
        snp_ids = session.get('snp_ids')
        combined_data = session.get('stats_data')

        # retrive population list from population comparison template 
        request_data = request.get_json()
        selected_populations = request_data.get('selected_populations')

        if not snp_ids or not selected_populations:
            return jsonify({"message": "No plot available"}), 400

        if all(combined_data[population][snp_id]['nsl'] == 'N/A' for population in selected_populations for snp_id in snp_ids):
            return jsonify({"message": "No plot available"}), 400

        # get nSL data from combined_data
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

        df = pd.DataFrame(plot_data)

        # bar chart 
        fig = px.bar(df, x="SNP ID", y="nSL", color="Population", barmode="group",
                     labels={"nSL": "nSL Value", "SNP ID": "SNPs", "Population": "Population"})
        fig.update_layout(title="nSL Values for Selected SNPs by Population", xaxis_title="SNP ID", yaxis_title="nSL Value")

        fig.add_hline(y=2, line_dash="dash", line_color="black")
        fig.add_hline(y=-2, line_dash="dash", line_color="black")

        # convert the bar chart to HTML for embedding
        plot_html = fig.to_html(full_html=False)

        return plot_html

    except Exception as e:
        return jsonify({"message": "Error generating nSL plot. Please try again later."}), 500
