from flask import Blueprint, render_template
from ..db_api.db_api import db

gene_bp = Blueprint('gene', __name__)

@gene_bp.route('/gene/<gene_symbol>')
def gene_details(gene_symbol):
    try:
        db.db_open()
        df = db.get_gene_annotations_by_gene_symbol(gene_symbol)
        if df is not None and not df.empty:
            gene_info = df.to_dict('records')  # Convert DataFrame to list of dicts
            return render_template('gene.html', gene_symbol=gene_symbol, gene_info=gene_info)
        else:
            return f"No gene details found for {gene_symbol}"
    except Exception as e:
        print(f"Error fetching gene details: {e}")
        return f"Error fetching gene details for {gene_symbol}"
    finally:
        db.db_close()
