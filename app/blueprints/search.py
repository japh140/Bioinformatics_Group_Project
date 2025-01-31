import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Define the Blueprint for 'search'
search_bp = Blueprint('search', __name__)

class dbclass(object):
    def __init__(db):
        db.dbconnection = ''

    def db_open(db,dblocation):
        db.dbconnection = sqlite3.connect(dblocation)

    def db_close(db):
        db.dbconnection.close()

    def db_home_page_query(db,querystring):
        query = 'SELECT SNP_Associations.snp_id as snp_associations_snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, ' \
        + 'gene_symbol, gene_id, chromosomal_locus, Gene_Annotations.snp_id as gene_annotations_snp_id, pathway, go_term, category, specificity ' \
        + 'FROM SNP_Associations ' \
        + 'LEFT JOIN Gene_Annotations ON SNP_Associations.snp_id = Gene_Annotations.snp_id ' \
        + 'WHERE SNP_Associations.snp_id LIKE ' + '"%' + querystring + '%" ' \
        + 'OR SNP_Associations.position = ' + '"' + querystring + '" ' \
        + 'OR SNP_Associations.mapped_gene LIKE ' + '"%' + querystring + '%" '
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df

db = dbclass()
database_location = 'project.db'
#db.db_open(database_location)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'

protein_table_finename = 'protein_table.tsv'

class QueryForm(FlaskForm):
    search_name = StringField('Enter a search term (SNP name, chromosome start, mapped gene name): ',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    form = QueryForm()
    search_name = None
    if form.validate_on_submit():
        search_name = form.search_name.data
        print('\n\n\n'+search_name+'\n\n\n')
        return redirect(url_for('protein', search_name=search_name))
    return render_template('project_index.html', form=form, search_name=search_name)

@app.route('/protein/<search_name>')
def protein(search_name):
    db.db_open(database_location)
    df = db.db_home_page_query(search_name) 
    db.db_close()
    print (df)
    print (df.columns)
    try:
        return render_template('project_view.html',  tables=[df.to_html(classes='data')], header="true")
        #row = df.iloc[0]
        #return render_template('project_view2.html', name=search_name, snp_associations_snp_id=row.snp_associations_snp_id, chromosome=row.chromosome, \
        #    position=row.position, p_value=row.p_value, mapped_gene=row.mapped_gene, phenotype=row.phenotype, population=row.population, \
        #    gene_symbol=row.gene_symbol, gene_id=row.gene_id, chromosomal_locus=row.chromosomal_locus, gene_annotations_snp_id=row.gene_annotations_snp_id, \
        #    pathway=row.pathway, go_term=row.go_term, category=row.category, specificity=row.specificity)
    except:
        return "We don't have any information about %s." % search_name

