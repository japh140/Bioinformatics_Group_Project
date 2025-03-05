from flask import Blueprint, render_template, url_for, redirect
from flask import send_file, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError
import io
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
                #if df is not None and not df.empty:
                    #print("Found SNPs in coordinates:", df['snp_id'].unique())
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



# Stats Table 
@snp_bp.route('/population-comparison', methods=['POST'])
def population_comparison():
    try:
        # retrieve SNP IDs from results template and population list from population comparison template 
        snp_ids = request.form.getlist('snp_ids') 
        selected_populations = request.form.getlist('selected_population')  

        if not snp_ids:
            raise ValueError("No SNP IDs provided.")
        
        if not selected_populations:
            selected_populations = ['Bengali', 'Gujarati', 'Punjabi', 'Telugu']

        if not selected_populations:
            raise ValueError("No population selected.")

        # fetch FST and nSL values from the database 
        combined_data = {}
        
        for population in selected_populations:
            combined_data[population] = {}
            for snp_id in snp_ids:
                stats_df = db.get_stats_by_snp_and_population(snp_id, population, 'Northern Europeans from Utah')

                if stats_df is not None and not stats_df.empty:
                    fst_value = stats_df['FST'].values[0] if stats_df['FST'].values[0] != 'N/A' else 'N/A'
                    nsl_value = stats_df['NSL'].values[0] if stats_df['NSL'].values[0] != 'N/A' else 'N/A'
                    combined_data[population][snp_id] = {"fst": fst_value, "nsl": nsl_value}
                else:
                    combined_data[population][snp_id] = {"fst": 'N/A', "nsl": 'N/A'}


        valid_data = any(
            value['fst'] != 'N/A' for population in combined_data for value in combined_data[population].values()
        )
        
        # raise error if no valid data found 
        if not valid_data:
            print("Warning: No valid FST data found for the selected SNPs and populations.")
        
        # store stats data and snp list in session
        session['stats_data'] = combined_data
        session['snp_ids'] = snp_ids

        # send stats data (fst_data) to frontend 
        return render_template('homepage/population_comparison.html', 
                              fst_data=combined_data, 
                              snp_ids=snp_ids)

    except Exception as e:
        return render_template('homepage/population_comparison.html', 
                               message=f"Error: {str(e)}. Please try again later.")



# Download Button
@snp_bp.route('/download-snp-data', methods=['POST'])
def download_snp_data():
    try:
        # retrieve stats and snp data from the session
        fst_data = session.get('stats_data', {})  # combined FST and nSL data
        snp_ids = session.get('snp_ids', [])  
        request_data = request.get_json()
        selected_populations = request_data.get('selected_populations')  # retrived from population_comparison template 

        if not fst_data or not snp_ids or not selected_populations:
            raise ValueError("No data found in session.")

        output = io.StringIO()  

        # headers
        output.write("SNP ID\tChromosome\tPosition\tP-value\tMapped Genes\tPhenotype\tPopulation\tFST Value\tnSL Value\n")

        for snp_id in snp_ids:
            snp_info = db.get_snp_by_id(snp_id)  
            if snp_info is None or snp_info.empty:
                continue  

            snp_details = snp_info.iloc[0]

            # remove commas from mapped genes 
            mapped_genes = snp_details.get('mapped_gene', [])
            if isinstance(mapped_genes, list):
                mapped_genes_str = ' '.join(mapped_genes) 
            else:
                mapped_genes_str = str(mapped_genes)  


            for population in selected_populations:
                fst_value = fst_data.get(population, {}).get(snp_id, {}).get('fst', 'N/A')
                nsl_value = fst_data.get(population, {}).get(snp_id, {}).get('nsl', 'N/A')

                output.write(
                    f"{snp_details.get('snp_id', 'N/A')}\t"
                    f"{snp_details.get('chromosome', 'N/A')}\t"
                    f"{snp_details.get('position', 'N/A')}\t"
                    f"{snp_details.get('p_value', 'N/A')}\t"
                    f"{mapped_genes_str}\t" 
                    f"{snp_details.get('phenotype', 'N/A')}\t"
                    f"{population}\t"  
                    f"{fst_value}\t"   
                    f"{nsl_value}\n"   
                )

        # calculate average and standard deviation of FST and nSL values
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

        average_fst = np.mean(fst_values) if fst_values else 0
        std_dev_fst = np.std(fst_values) if fst_values else 0
        average_nsl = np.mean(nsl_values) if nsl_values else 0
        std_dev_nsl = np.std(nsl_values) if nsl_values else 0

        # output
        output.write("\n")  
        output.write("\t\t\t\t\t\t\tFST\tnSL\n")  
        output.write(f"Mean\t\t\t\t\t\t\t{average_fst:.4f}\t{average_nsl:.4f}\n")
        output.write(f"Standard Deviation\t\t\t\t\t{std_dev_fst:.4f}\t{std_dev_nsl:.4f}\n")

        output.seek(0)  

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/plain', 
            as_attachment=True,
            download_name="snp_data.txt"  
        )

    except Exception as e:
        return render_template(
            'homepage/search_error.html',
            search_type='population',
            search_term='N/A',
            error_message="Error generating SNP data. Please try again later.")