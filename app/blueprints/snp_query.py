from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError
from app import db

snp_bp = Blueprint('snp_query', __name__)

# Define the SNP_Associations model
class SNP_Associations(db.Model):
    __tablename__ = 'SNP_Associations'
    snp_id = db.Column(db.String, primary_key=True)
    chromosome = db.Column(db.String)
    position = db.Column(db.Integer)
    p_value = db.Column(db.Float)
    mapped_gene = db.Column(db.String)
    phenotype = db.Column(db.String)
    population = db.Column(db.String)

# Custom validation function
def validate_search_term(form, field):
    if form.search_type.data == 'rs':
        if not field.data.startswith('rs'):
            raise ValidationError('RS numbers must start with "rs" followed by numbers only.')
    elif form.search_type.data == 'coordinates':
        if not ':' in field.data:
            raise ValidationError('Format must be "chrN:start-end".')
    elif form.search_type.data == 'gene':
        if not field.data.isalnum():
            raise ValidationError('Invalid gene name. Use only letters and numbers.')

# Form definition
class SNPSearchForm(FlaskForm):
    search_type = SelectField('Search Type',
        choices=[
            ('rs', 'RS Number'),
            ('coordinates', 'Genomic Coordinates'),
            ('gene', 'Gene Name')
        ],
        validators=[InputRequired()])
    search_term = StringField('Search Term',
        validators=[InputRequired(), validate_search_term])
    submit = SubmitField('Search')

# Search function
def get_snp_data(search_type, search_term):
    if search_type == 'rs':
        snps = SNP_Associations.query.filter_by(snp_id=search_term).all()
    elif search_type == 'gene':
        snps = SNP_Associations.query.filter(SNP_Associations.mapped_gene.like(f"%{search_term}%")).all()
    elif search_type == 'coordinates':
        try:
            chromosome, position = search_term.split(':')
            snps = SNP_Associations.query.filter_by(chromosome=chromosome, position=int(position)).all()
        except ValueError:
            snps = []
    else:
        snps = []

    results = []
    for snp in snps:
        results.append({
            'snp_id': snp.snp_id,
            'chromosome': snp.chromosome,
            'position': snp.position,
            'p_value': snp.p_value,
            'mapped_genes': snp.mapped_gene.split(",") if snp.mapped_gene else [],
            'phenotype': snp.phenotype,
            'population': snp.population
        })
    return results

# Routes
@snp_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SNPSearchForm()
    if form.validate_on_submit():
        search_type = form.search_type.data
        search_term = form.search_term.data
        results = get_snp_data(search_type, search_term)
        if not results:
            flash("No results found.", "error")
            return redirect(url_for('snp_query.index'))
        return render_template('display.html', results=results)
    return render_template('index.html', form=form)