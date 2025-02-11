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

        # Fetch summary statistics and SNP details for the selected SNP and population
        # No need for explicit db connection open/close, we use get_db() from db_api
        snp_info = db.get_snp_and_gene_by_snp(snp_id)  # SNP info like chromosome, gene, phenotype
        stats_df = db.get_summary_stats_by_snp(snp_id)  # Summary statistics for the selected SNP

        if snp_info is None or snp_info.empty:
            return jsonify({"error": "No SNP information found for the selected SNP ID"}), 404

        if stats_df is None or stats_df.empty:
            return jsonify({"error": "No summary statistics found for the selected SNP"}), 404

        # Prepare the data for the CSV file
        output = io.StringIO()
        
        # Extract SNP details (first row for SNP info)
        snp_details = snp_info.iloc[0]  # Get the first entry of the SNP info
        output.write(f"SNP ID: {snp_details.get('snp_associations_snp_id', '')}\n")
        output.write(f"Chromosome: {snp_details.get('chromosome', '')}\n")
        output.write(f"Position: {snp_details.get('position', '')}\n")
        output.write(f"P-value: {snp_details.get('p_value', '')}\n")
        output.write(f"Mapped Genes: {snp_details.get('mapped_gene', '')}\n")
        output.write(f"Phenotype: {snp_details.get('phenotype', '')}\n\n")
        
        # Add population-specific summary statistics (if available)
        output.write("Population | Tajima's D | XP-EHH | HIS | Nucleotide Diversity\n")

        # Filter by population if specified
        if population:
            stats_df = stats_df[stats_df['population'] == population]

        # Write the data rows for the selected SNP
        for _, row in stats_df.iterrows():
            output.write(f"{row.get('population', '')} | {row.get('tajimas_d', '')} | "
                         f"{row.get('xp_ehh', '')} | {row.get('his', '')} | "
                         f"{row.get('nucleotide_diversity', '')}\n")

        # Prepare the file for download
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),  # Convert to bytes for sending
            mimetype='text/plain',  # Set MIME type to text
            as_attachment=True,
            download_name=f'{snp_id}_summary_statistics.txt'  # Specify .txt extension
        )

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
