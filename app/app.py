from flask import Flask
from blueprints.snp_query.views import snp_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-here'  # Change this in production

app.register_blueprint(snp_bp)

if __name__ == '__main__':
    app.run(debug=True)
