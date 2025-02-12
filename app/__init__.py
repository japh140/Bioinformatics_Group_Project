from flask import Flask
try:
    # try absolute path first
    from app.blueprints.snp_query.views import snp_bp
    from app.blueprints.snp_query.gene import gene_bp
    from app.blueprints.snp_query.download import download_bp
    from app.blueprints.db_api.db_api import db_api, init_db_teardown
except ImportError:
    # fall back to relative path
    from blueprints.snp_query.views import snp_bp
    from blueprints.snp_query.gene import gene_bp
    from blueprints.snp_query.download import download_bp
    from blueprints.db_api.db_api import db_api, init_db_teardown
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(snp_bp)
app.register_blueprint(db_api)
app.register_blueprint(gene_bp)
app.register_blueprint(download_bp)

init_db_teardown(app)