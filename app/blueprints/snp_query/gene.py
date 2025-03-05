from flask import Blueprint, render_template
from ..db_api.db_api import db

gene_bp = Blueprint('gene', __name__)

@gene_bp.route('/gene/<gene_symbol>')
def gene_details(gene_symbol):
    try:
        df = db.get_gene_annotations_by_gene_symbol(gene_symbol)
        
        if df is not None and not df.empty:
            # drop duplicates
            df = df.drop_duplicates(subset='gene_symbol', keep='first')  

            gene_info = df.to_dict('records')
            return render_template('gene.html', gene_symbol=gene_symbol, gene_info=gene_info)
        else:
            return render_template('gene_error.html', gene_name=gene_symbol)
    except Exception as e:
        print(f"Error fetching gene details: {e}")
        return render_template('gene_error.html', gene_name=gene_symbol)
