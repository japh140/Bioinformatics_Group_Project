import os

class Config:
    # Flask base config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')  # Required for Flask-WTF forms
    DEBUG = True  # Enable debug mode
    CSRF_ENABLED = True  # Enable CSRF protection

    # Database settings
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'project.db')  # Path to the SQLite database

    # Logging config
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_FILE = 'app.log'

    @staticmethod
    def init_app(app):
        import logging
        logging.basicConfig(filename=app.config['LOGGING_FILE'],
                            level=app.config['LOGGING_LEVEL'],
                            format=app.config['LOGGING_FORMAT'])

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'test_project.db')  # Test database
