class Config:
    SECRET_KEY = 'your-secret-key-here'         # Secret Key
    DATABASE_PATH = 'app/project.db'                # location of the SQlite database
    SUPER_POPULATION = 'South Asian Ancestry'   # Superpopulation to examine 
    QUERY_LIMIT = '25'                          # Global limit on number of results returned by SQL queries