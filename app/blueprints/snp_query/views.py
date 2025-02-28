from flask import Blueprint, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError
import io
import csv
from flask import send_file, request,session
import numpy as np


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
                # Add this debug print
                if df is not None and not df.empty:
                    print("Found SNPs in coordinates:", df['snp_id'].unique())
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


@snp_bp.route('/population-comparison', methods=['POST'])
def population_comparison():
    try:
        # Step 1: Retrieve SNP IDs and selected populations from the form submission
        snp_ids = request.form.getlist('snp_ids')  # Expecting SNP IDs to be sent as a list
        selected_populations = request.form.getlist('selected_population')  # Get selected populations as a list

        # Debugging prints
        print("SNP IDs received:", snp_ids)
        print("Selected Populations:", selected_populations)

        # If no SNP IDs or populations are selected, raise an error
        if not snp_ids:
            raise ValueError("No SNP IDs provided.")
        
        # If no population is selected, default to all populations
        if not selected_populations:
            selected_populations = ['Bengali', 'Gujarati', 'Punjabi', 'Telugu']

        # If no selected populations after fallback, raise an error
        if not selected_populations:
            raise ValueError("No population selected.")

        # Step 2: Fetch FST and NSL values for each SNP ID and selected population
        combined_data = {}
        
        for population in selected_populations:
            combined_data[population] = {}
            for snp_id in snp_ids:
                print(f"Fetching FST and NSL for SNP {snp_id} and Population {population}")
                # Fetch both FST and NSL data from the database
                stats_df = db.get_stats_by_snp_and_population(snp_id, population, 'Northern Europeans from Utah')
                print(f"FST & NSL data for SNP {snp_id} and Population {population}: {stats_df}")

                # Process the FST and NSL data
                if stats_df is not None and not stats_df.empty:
                    fst_value = stats_df['FST'].values[0] if stats_df['FST'].values[0] != 'N/A' else 'N/A'
                    nsl_value = stats_df['NSL'].values[0] if stats_df['NSL'].values[0] != 'N/A' else 'N/A'
                    combined_data[population][snp_id] = {"fst": fst_value, "nsl": nsl_value}
                else:
                    combined_data[population][snp_id] = {"fst": 'N/A', "nsl": 'N/A'}

        # Check if any valid data was found
        valid_data = any(
            value['fst'] != 'N/A' for population in combined_data for value in combined_data[population].values()
        )
        
        # If no valid data exists, raise an error to notify the user
        if not valid_data:
            print("Warning: No valid FST data found for the selected SNPs and populations.")

        # Debugging: Check the final data structure
        print("Fetched Combined Data:", combined_data)

        session['stats_data'] = combined_data
        session['snp_ids'] = snp_ids

        # Step 3: Render the population_comparison.html template directly with the FST and NSL data
        return render_template('homepage/population_comparison.html', 
                              fst_data=combined_data, 
                              snp_ids=snp_ids, 
                              plot_fst_url=url_for('plot.plot_fst'))

    except Exception as e:
        # Debugging error message
        print(f"Error: {str(e)}")

        # Handle error and provide user-friendly message
        return render_template('homepage/population_comparison.html', 
                               message=f"Error: {str(e)}. Please try again later.")




# Download Button
@snp_bp.route('/download-snp-data', methods=['POST'])
def download_snp_data():
    try:
        # Step 1: Retrieve data from the session
        fst_data = session.get('stats_data', {})  # Combined FST and nSL data
        snp_ids = session.get('snp_ids', [])    # List of SNP IDs
        request_data = request.get_json()
        selected_populations = request_data.get('selected_populations')  # Selected populations

        if not fst_data or not snp_ids or not selected_populations:
            raise ValueError("No data found in session.")

        # Step 2: Prepare the table data
        output = io.StringIO()  # Use StringIO for text-based content

        # Write the table header
        output.write("SNP ID\tChromosome\tPosition\tP-value\tMapped Genes\tPhenotype\tPopulation\tFST Value\tnSL Value\n")

        # Fetch and write data for each SNP ID and population
        for snp_id in snp_ids:
            # Fetch SNP details from the database
            snp_info = db.get_snp_by_id(snp_id)  # Fetch SNP details from SNP_Associations table
            if snp_info is None or snp_info.empty:
                print(f"No SNP information found for SNP ID: {snp_id}")
                continue  # Skip this SNP if no data is found

            # Get the first row for common data
            snp_details = snp_info.iloc[0]

            # Process mapped genes to remove commas
            mapped_genes = snp_details.get('mapped_gene', [])
            if isinstance(mapped_genes, list):
                mapped_genes_str = ' '.join(mapped_genes)  # Join genes with a space instead of a comma
            else:
                mapped_genes_str = str(mapped_genes)  # Fallback if mapped_gene is not a list

            # Write data for each population
            for population in selected_populations:
                # Get FST and nSL values for the current SNP and population
                fst_value = fst_data.get(population, {}).get(snp_id, {}).get('fst', 'N/A')
                nsl_value = fst_data.get(population, {}).get(snp_id, {}).get('nsl', 'N/A')

                # Write the row to the output
                output.write(
                    f"{snp_details.get('snp_id', 'N/A')}\t"
                    f"{snp_details.get('chromosome', 'N/A')}\t"
                    f"{snp_details.get('position', 'N/A')}\t"
                    f"{snp_details.get('p_value', 'N/A')}\t"
                    f"{mapped_genes_str}\t"  # Use the processed mapped genes
                    f"{snp_details.get('phenotype', 'N/A')}\t"
                    f"{population}\t"  # Add population column
                    f"{fst_value}\t"   # Add FST value
                    f"{nsl_value}\n"   # Add nSL value
                )

        # Step 3: Calculate average and standard deviation of FST and nSL values
        fst_values = [
            fst_data[population][snp_id]['fst']
            for population in selected_populations
            for snp_id in snp_ids
            if isinstance(fst_data[population][snp_id]['fst'], (int, float))
        ]
        nsl_values = [
            fst_data[population][snp_id]['nsl']
            for population in selected_populations
            for snp_id in snp_ids
            if isinstance(fst_data[population][snp_id]['nsl'], (int, float))
        ]

        # Calculate statistics
        average_fst = np.mean(fst_values) if fst_values else 0
        std_dev_fst = np.std(fst_values) if fst_values else 0
        average_nsl = np.mean(nsl_values) if nsl_values else 0
        std_dev_nsl = np.std(nsl_values) if nsl_values else 0

        # Step 4: Append statistics to the output in the specified format
        output.write("\n")  # Add a newline for separation
        output.write("\t\t\t\t\t\t\tFST\tnSL\n")  # Header for statistics
        output.write(f"Mean\t\t\t\t\t\t\t{average_fst:.4f}\t{average_nsl:.4f}\n")
        output.write(f"Standard Deviation\t\t\t\t\t{std_dev_fst:.4f}\t{std_dev_nsl:.4f}\n")

        output.seek(0)  # Reset the cursor to the start of the StringIO buffer

        # Step 5: Send the plain text file as a download
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/plain',  # Set MIME type to plain text
            as_attachment=True,
            download_name="snp_data.txt"  # Specify the file name
        )

    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging statement
        return render_template(
            'homepage/search_error.html',
            search_type='population',
            search_term='N/A',
            error_message="Error generating SNP data. Please try again later.")