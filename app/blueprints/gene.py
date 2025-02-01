from flask import Blueprint, jsonify, request
from app import db

# Create a Blueprint for gene routes
gene_bp = Blueprint('gene', __name__)

@gene_bp.route('/api/gene-info', methods=['GET'])
def get_gene_info():
    gene_symbol = request.args.get('gene_symbol')
    if not gene_symbol:
        return jsonify({"error": "Gene symbol is required"}), 400

    # Query the database
    query = '''
        SELECT gene_symbol, gene_id, pathway, go_term, category
        FROM Gene_Annotations
        WHERE gene_symbol = ?
    '''
    result = db.engine.execute(query, (gene_symbol,))
    gene_data = result.fetchone()

    if gene_data:
        # Convert the result to a dictionary
        gene_info = {
            "gene_symbol": gene_data[0],
            "gene_id": gene_data[1],
            "pathway": gene_data[2],
            "go_term": gene_data[3],
            "category": gene_data[4]
        }
        return jsonify(gene_info)
    else:
        return jsonify({"error": "Gene not found"}), 404
