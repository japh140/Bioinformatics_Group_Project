from flask import Blueprint, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError

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
                return render_template('homepage/search_error.html',
                                   search_type=search_type,
                                   search_term=search_term,
                                   error_message="Invalid search type")

        if df is not None and not df.empty:
            # group by snp id to combine multiple entries
            results = []
            grouped = df.groupby('snp_id')

            for snp_id, group in grouped:
                # get the common values (should be same for all entries of same snp)
                first_row = group.iloc[0]
                result = {
                    'snp_id': snp_id,
                    'chromosome': first_row.chromosome,
                    'position': first_row.position,
                    'p_values': group.p_value.unique().tolist(),  # list of all unique p values
                    'mapped_genes': group.mapped_gene.unique().tolist(),  # list of all unique genes
                    'populations': group.population.unique().tolist(),  # list of all unique populations
                    'phenotype': first_row.phenotype
                }
                results.append(result)

            return render_template('homepage/results.html',
                                   search_type=search_type,
                                   search_term=search_term,
                                   results=results)
        else:
            return render_template('homepage/search_error.html',
                                   search_type=search_type,
                                   search_term=search_term,
                                   error_message="No results found")

    except ValueError as ve:
        return render_template('homepage/search_error.html',
                               search_type=search_type,
                               search_term=search_term,
                               error_message=str(ve))
    except IndexError:
        return render_template('homepage/search_error.html',
                               search_type=search_type,
                               search_term=search_term,
                               error_message="No results found")
    except Exception as e:
        return render_template('homepage/search_error.html',
                               search_type=search_type,
                               search_term=search_term,
                               error_message="Error processing search. Please try again later.")

@snp_bp.route('/population-comparison/<search_data>')
def population_comparison(search_data):
    try:
        # this will be where we'll eventually process the real SNP statistics
        # for now return placeholder page

        population_info = {
            'Punjabi': 'Sample population from Punjab region (exact sampling location TBD)',
            'Telugu': 'Sample population of Telugu speakers (exact sampling location TBD)',
            'Bengali': 'Sample population from Bengal region (exact sampling location TBD)',
            'Gujarati': 'Sample population from Gujarat region (exact sampling location TBD)',
            'Tamil': 'Sample population of Tamil speakers (exact sampling location TBD)'
        }

        # placeholder data structure - will change when real stats are ready
        populations = {
            'Punjabi': {'description': population_info['Punjabi']},
            'Telugu': {'description': population_info['Telugu']},
            'Bengali': {'description': population_info['Bengali']},
            'Gujarati': {'description': population_info['Gujarati']},
            'Tamil': {'description': population_info['Tamil']}
        }

        return render_template('homepage/population_comparison.html',
                               populations=populations,
                               message="Statistics for selected SNPs will be available soon.")
    except Exception as e:
        return f"Error retrieving population statistics: {e}"