from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Regexp, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

def validate_search_term(form, field):
    print(f"Validating search term: {field.data} for type: {form.search_type.data}")  # Add this line
    if form.search_type.data == 'rs':
        if not Regexp('^rs\d+$').regex.match(field.data):
            raise ValidationError('RS numbers must start with "rs" followed by numbers only')
    if form.search_type.data == 'coordinates':
        if not Regexp('^chr([1-9]|1[0-9]|2[0-2]|[XYM]):\d+-\d+$').regex.match(field.data):
            raise ValidationError('Format must be "chrN:start-end" (N = 1-22, X, Y, M; start/end = positive integers).')
    if form.search_type.data == 'gene':
        if not Regexp('^[A-Za-z][A-Za-z0-9_-]*$').regex.match(field.data):
            raise ValidationError('Invalid gene name. Use only letters, numbers, underscores, or hyphens, starting with a letter.')

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
            validate_search_term  # Add our custom validator
        ])
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SNPSearchForm()
    if form.validate_on_submit():
        search_type = form.search_type.data
        search_term = form.search_term.data
        return redirect(url_for('search_results',
                              search_type=search_type,
                              search_term=search_term))
    return render_template('homepage/index.html', form=form)

@app.route('/search/<search_type>/<search_term>')
def search_results(search_type, search_term):
    # Mock data for now
    results = {
        'snp_id': search_term if search_type == 'rs' else 'rs12345',
        'position': 'chr10:123456',
        'p_value': '0.0001',
        'mapped_genes': ['TCF7L2']
    }
    return render_template('homepage/results.html',
                         search_type=search_type,
                         search_term=search_term,
                         results=results)

if __name__ == '__main__':
    app.run(debug=True)
