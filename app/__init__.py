from flask import Flask
from app.blueprints.snp_query.views import snp_bp
from app.blueprints.db_api.db_api import db_api
from app.blueprints.snp_query.gene import gene_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(snp_bp)
app.register_blueprint(db_api)
app.register_blueprint(gene_bp)