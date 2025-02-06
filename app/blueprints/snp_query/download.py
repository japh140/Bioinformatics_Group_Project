from flask import Blueprint, request, jsonify, send_file
import io
import csv
import pandas as pd
from ..db_api.db_api import db

# Create a Blueprint for the download functionality
download_bp = Blueprint('download', __name__)

@download_bp.route('/download', methods=['POST'])
def download_data():
    try:
        # Get the SNP ID and population from the form
        snp_id = request.form.get('snp_id')  # SNP ID selected for download
        population = request.form.get('population', None)  # Population selected for download (if any)

        # Fetch summary statistics for the selected SNP and population
        # No need for explicit db connection open/close, we use get_db() from db_api
        stats_df = db.get_summary_stats_by_snp(snp_id)
        if stats_df is None or stats_df.empty:
            return jsonify({"error": "No summary statistics found for the selected SNP"}), 404

        # Filter by population if specified
        if population:
            stats_df = stats_df[stats_df['population'] == population]

        # Prepare the data for the CSV file
        output = io.StringIO()
        writer = csv.writer(output)

        # Write the header
        writer.writerow(['SNP ID', 'Population', 'Tajimas D', 'XP-EHH', 'HIS', 'Nucleotide Diversity'])

        # Write the data rows for the selected SNP
        for _, row in stats_df.iterrows():
            writer.writerow([
                row.get('snp_id', ''),
                row.get('population', ''),
                row.get('tajimas_d', ''),
                row.get('xp_ehh', ''),
                row.get('his', ''),
                row.get('nucleotide_diversity', '')
            ])

        # Prepare the file for download
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{snp_id}_summary_statistics.csv'
        )
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
