from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError

from ..db_api.db_api import db

gene_bp = Blueprint('gene_query', __name__)

def validate_search_term(form, field):  # Check if search term is valid for gene
    print(f"Validating search term: {field.data} for type: {form.search_type.data}")
    if not Regexp('^[A-Za-z][A-Za-z0-9_-]*$').regex.match(field.data):
        raise ValidationError('Invalid gene name. Use only letters, numbers, underscores, or hyphens, starting with a letter.')

class GeneSearchForm(FlaskForm):
    search_term = StringField('Gene Symbol:',
        validators=[InputRequired(), validate_search_term])
    submit = SubmitField('Search')

@gene_bp.route('/', methods=['GET', 'POST'])
def index():
    form = GeneSearchForm()
    if form.validate_on_submit():
        search_term = form.search_term.data
        return redirect(url_for('gene_query.search_results', search_term=search_term))
    return render_template('homepage/index.html', form=form)

@gene_bp.route('/search/<search_term>')
def search_results(search_term):
    try:
        
        db.db_open()
        
        # Query the database for gene annotations
        df = db.get_gene_annotations_by_gene_symbol(search_term)
        
        # Only fetch necessary columns: gene_symbol, gene_id, pathway, go_term, category
        if df is not None and not df.empty:
            gene_info = df[['gene_symbol', 'gene_id', 'pathway', 'go_term', 'category']].to_dict('records')
            return render_template('homepage/gene_results.html', search_term=search_term, gene_info=gene_info)
        else:
            return f"No details found for gene {search_term}"

    except Exception as e:
        print(f"Error processing search for {search_term}: {e}")
        return f"Error fetching data for {search_term}"

    finally:
        db.db_close()
