import os
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config is not None:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Register the blueprint
    from app.blueprints.snp_query import snp_bp
    app.register_blueprint(snp_bp)
    

    return app
