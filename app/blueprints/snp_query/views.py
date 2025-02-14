from flask import Blueprint, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError
import io
import csv
from flask import send_file, request
import logging


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
                # first get populations for this snp
                populations = group.population.unique()

                # for each population
                for pop in populations:
                    # get all rows for this snp and population
                    pop_data = group[group.population == pop]

                    # get first row for common data
                    first_row = pop_data.iloc[0]

                    result = {
                        'snp_id': snp_id,
                        'chromosome': first_row.chromosome,
                        'position': first_row.position,
                        'p_values': pop_data.p_value.unique().tolist(),  # p-values for this population
                        'mapped_genes': pop_data.mapped_gene.unique().tolist(),
                        'population': pop,  # single population
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
        # Fetch FST and population data using the allele frequency table
        fst_data_df = db.get_allele_frequency_by_snp(search_data)

        # Initialize populations dictionary
        populations = {}

        # Check if FST data is available
        if fst_data_df is not None and not fst_data_df.empty:
            for index, row in fst_data_df.iterrows():
                population = row['population']
                fst_value = row['FST']
                
                # Handle None values
                if population is None:
                    population = "Unknown Population"
                
                if fst_value is None:
                    fst_value = "N/A"  # Default value for missing FST data
                
                # Add population and FST data to dictionary
                populations[population] = {'fst': fst_value, 'description': f'Sample population description for {population}'}

            # Render the population comparison page with FST data
            return render_template('homepage/population_comparison.html',
                                   populations=populations,
                                   search_data=search_data,
                                   message="Population comparison statistics are displayed below.")
        else:
            # Handle case where no FST data is found
            return render_template('homepage/population_comparison.html',
                                   populations={},
                                   search_data=search_data,
                                   message="No population data found for the given SNP.")
    except Exception as e:
        # Log the error or print for debugging
        print(f"Error retrieving population statistics: {e}")
        return render_template('homepage/population_comparison.html',
                               populations={},
                               search_data=search_data,
                               message="Error retrieving population statistics. Please try again later.")

    



# Download Button
logging.basicConfig(level=logging.DEBUG)

@snp_bp.route('/download-snp-data', methods=['POST'])
def download_snp_data():
    try:
        # Step 1: Get the SNP ID from the form input
        snp_id = request.form.get('snp_id')
        print(f"Received SNP ID: {snp_id}")  # Debugging statement
        
        if not snp_id:
            raise ValueError("No SNP ID provided.")
        
        # Step 2: Fetch SNP Data from the Database using the allele_frequency table
        snp_data = db.get_allele_frequency_by_snp(snp_id)
        print(f"SNP Data fetched: {snp_data}")  # Debugging statement
        
        if snp_data is None or snp_data.empty:
            print("No data found for SNP ID.")  # Debugging statement
            raise ValueError(f"No data found for SNP ID: {snp_id}")

        # Step 3: Prepare Plain Text Data
        print("Creating plain text data...")  # Debugging statement
        output = io.StringIO()  # Use StringIO for text-based content
        
        # Add the headers manually
        output.write("SNP ID | Population | FST\n")

        # Write the data rows
        for index, row in snp_data.iterrows():
            output.write(f"{row['snp_id']} | {row['population']} | {row['FST']}\n")
        
        output.seek(0)  # Reset the cursor to the start of the StringIO buffer
        
        # Step 4: Send the plain text file as a download
        print("Sending plain text file as response...")  # Debugging statement
        return send_file(io.BytesIO(output.getvalue().encode()), 
                         mimetype='text/plain',  # Set MIME type to plain text
                         as_attachment=True, 
                         download_name=f"{snp_id}_population_data.txt")  # Specify .txt extension

    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging statement
        return render_template('homepage/search_error.html', 
                               search_type='population', 
                               search_term=snp_id, 
                               error_message="Error generating SNP data. Please try again later.")
