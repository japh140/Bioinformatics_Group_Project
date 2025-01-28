from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def get_snp_data(search_type, search_term):
    # TODO: Replace this with real database query; for now return mock data in the expected format
    return {
        'snp_id': search_term,
        'position': 'chr10:123456',
        'p_value': '0.0001',
        'mapped_genes': ['TCF7L2']
    }
@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['search_type']
    search_term = request.form['search_term']

    results = get_snp_data(search_type, search_term)
    return render_template('results.html',
                           search_type=search_type,
                           search_term=search_term,
                           results=results)
if __name__ == '__main__':
    app.run(debug=True)