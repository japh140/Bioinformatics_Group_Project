import os
from flask import Flask
from app.config import Config

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set up default config from Config class
    app.config.from_object(Config)

    if test_config is not None:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Register the blueprint
    from app.blueprints.search import search_bp
    app.register_blueprint(search_bp)

    return app
