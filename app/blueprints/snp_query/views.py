from flask import Blueprint, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError
import pandas as pd

try:
    # absolute import version
    from app.blueprints.db_api.db_api import db
except ImportError:
    # relative import version
    from ..db_api.db_api import db

snp_bp = Blueprint('snp_query', __name__)

def validate_search_term(form, field):
    try:
        if form.search_type.data == 'rs':
            if not Regexp('^rs\d+$').regex.match(field.data):
                raise ValidationError('RS numbers must start with "rs" followed by numbers only')
        if form.search_type.data == 'coordinates':
            if not (Regexp('^chr([1-9]|1[0-9]|2[0-2]|[XYM]):\d+-\d+$').regex.match(field.data) or
                    Regexp('^chr([1-9]|1[0-9]|2[0-2]|[XYM]):\d+$').regex.match(field.data)):
                raise ValidationError('Format must be either "chrN:position" or "chrN:start-end" (N = 1-22, X, Y, M)')
        if form.search_type.data == 'gene':
            if not Regexp('^[A-Za-z][A-Za-z0-9_-]*$').regex.match(field.data):
                raise ValidationError('Invalid gene name. Use only letters, numbers, underscores, or hyphens, starting with a letter.')
    except ValidationError:
        raise
    except Exception:
        raise ValidationError('Invalid input format')

class SNPSearchForm(FlaskForm):
    search_type = SelectField('Search Type',
        choices=[
            ('rs', 'RS Number'),
            ('coordinates', 'Genomic Coordinates'),
            ('gene', 'Gene Name')
        ])
    search_term = StringField('Search Term:',
        validators=[
            InputRequired(),
            validate_search_term
        ])
    submit = SubmitField('Search')

@snp_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SNPSearchForm()
    if form.validate_on_submit():
        search_type = form.search_type.data
        search_term = form.search_term.data
        return redirect(url_for('snp_query.search_results',
                              search_type=search_type,
                              search_term=search_term))
    return render_template('homepage/index.html', form=form)

@snp_bp.route('/search/<search_type>/<search_term>')
def search_results(search_type, search_term):
    try:
        match search_type:
            case 'rs':
                df = db.get_snp_by_id(search_term)
            case 'coordinates':
                # parse coordinates from search_term
                chrom = search_term.split(':')[0].replace('chr', '')
                if '-' in search_term:  # range format
                    start, end = map(int, search_term.split(':')[1].split('-'))
                else:  # single position
                    position = int(search_term.split(':')[1])
                    start = end = position
                df = db.get_snp_by_coordinates(chrom, start, end)
            case 'gene':
                df = db.get_snp_by_gene(search_term)
            case _:
                raise ValueError(f"Invalid search type: {search_type}")

        if df is not None and not df.empty:
            # Remove duplicates based on different combinations of columns:
            # 1. SNP ID and Population
            # 2. Gene Symbol (Mapped Gene) and Population
            # 3. Chromosome and Population
            df = df.drop_duplicates(subset=['snp_id', 'population'], keep='first')
            df = df.drop_duplicates(subset=['mapped_gene', 'population'], keep='first')
            df = df.drop_duplicates(subset=['chromosome', 'population'], keep='first')

            results = []
            for _, row in df.iterrows():
                results.append({
                    'snp_id': row.snp_id,
                    'chromosome': row.chromosome,
                    'position': row.position,
                    'p_value': row.p_value,
                    'mapped_genes': [row.mapped_gene] if row.mapped_gene else [],
                    'population': row.population,
                    'phenotype': row.phenotype
                })

            return render_template('homepage/results.html',
                                   search_type=search_type,
                                   search_term=search_term,
                                   results=results)
        else:
            return f"No results found for {search_term}"

    except ValueError as ve:
        return f"Invalid search parameters: {str(ve)}"
    except IndexError:
        return f"No results found for {search_term}"
    except Exception as e:
        return f"Error processing search for {search_term}. Please try again later."


@snp_bp.route('/population-comparison')
def population_comparison():
    try:
        df = db.get_population_stats()  # This should return a DataFrame with population data

        population_info = {
            'Punjabi': 'Sample population from Punjab region (exact sampling location TBD)',
            'Telugu': 'Sample population of Telugu speakers (exact sampling location TBD)',
            'Bengali': 'Sample population from Bengal region (exact sampling location TBD)',
            'Gujarati': 'Sample population from Gujarat region (exact sampling location TBD)',
            'Tamil': 'Sample population of Tamil speakers (exact sampling location TBD)'
        }

        populations = {}
        for _, row in df.iterrows():
            populations[row.population] = {
                'description': population_info[row.population],
                'tajimas_d': row.tajimas_d,
                'xp_ehh': row.xp_ehh,
                'his': row.his,
                'nucleotide_diversity': row.nucleotide_diversity
            }

        return render_template('homepage/population_comparison.html', populations=populations)
    except Exception as e:
        return f"Error retrieving population statistics: {e}"