import os

class Config:
    # Flask base config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    DEBUG = True
    CSRF_ENABLED = True

    # Database settings (Using Binds for multiple DBs)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'snp_data': 'sqlite:///data/snp_data.db',
        'selection_stats': 'sqlite:///data/selection_stats.db',
        'gene_annotations': 'sqlite:///data/gene_annotations.db'
    }

    # Custom settings
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
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
    SQLALCHEMY_BINDS = {
        'snp_data': os.environ.get('SNP_DATABASE_URL'),
        'selection_stats': os.environ.get('SELECTION_DATABASE_URL'),
        'gene_annotations': os.environ.get('GENE_DATABASE_URL')
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_BINDS = {
        'snp_data': 'sqlite:///data/test_snp_data.db',
        'selection_stats': 'sqlite:///data/test_selection_stats.db',
        'gene_annotations': 'sqlite:///data/test_gene_annotations.db'
    }

