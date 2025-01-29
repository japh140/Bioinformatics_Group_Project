# Flask and sqlAlchemy setup 
# Defines the database table 
# Defines the search function and conditional queries 
# Formats the results 
# Defines the search route
# Renders index.html template when user visits homepage
# Renders results.html template 
# Starts the flask application 

from flask import Flask, render_template, request
from app import db
from app.blueprints.snp_query.models import SNP_Associations

# Initialize the Blueprint
snp_query_bp = Blueprint('snp_query', __name__)


# Search function that handles SNP ID, gene name, or chromosome position
def get_snp_data(search_type, search_term):
    if search_type == 'snp_id':
        # Query by SNP ID
        snps = SNP_Associations.query.filter_by(snp_id=search_term).all()
    elif search_type == 'gene_name':
        # Query by mapped gene
        snps = SNP_Associations.query.filter(SNP_Associations.mapped_gene.like(f"%{search_term}%")).all()
    elif search_type == 'chromosome_position':
        # Query by chromosome and position (assuming 'position' is an integer)
        snps = SNP_Associations.query.filter_by(position=int(search_term)).all()
    else:
        snps = []

    # Prepare data in the expected format
    results = []
    for snp in snps:
        results.append({
            'snp_id': snp.snp_id,
            'position': f'{snp.chromosome}:{snp.position}',
            'p_value': snp.p_value,
            'mapped_genes': snp.mapped_gene.split(",") if snp.mapped_gene else []
        })

    return results


# Define the route for the homepage
@snp_query_bp.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['search_type']
    search_term = request.form['search_term']

    results = get_snp_data(search_type, search_term)
    if not results:
        return render_template('error.html', message= "No results found.")
    
    return render_template('results.html',
                           search_type=search_type,
                           search_term=search_term,
                           results=results)
