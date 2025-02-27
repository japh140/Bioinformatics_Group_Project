##
## DATABASE API
##

"""
##      get_snp_by_id(snpid):
"""
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population
##          FROM            SNP_Associations
##          WHERE:          snp_id LIKE "%<snpid>%"
##          ORDER BY        snp_id

"""
##      get_snp_by_gene(genename):
"""
##      query_string:       mapped_gene to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population
##          FROM            SNP_Associations
##          WHERE:          mapped_gene LIKE "%<genename>%"
##          ORDER BY        snp_id

"""
##      get_snp_by_coordinates(chromosome, start, end):
"""
##      chromosome:         snp_chromosomeid to query
##      start               starting chromosome position to query from
##      end                 ending chromosome position to query to
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population
##          FROM            SNP_Associations
##          WHERE:          WHERE chromosome = "<chromosome>" AND position >= <start> AND position <= <end>
##          ORDER BY        snp_id

"""
##      get_gene_annotations_by_gene_symbol(genename):
"""
##      query_string:       gene_symbol to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity
##          FROM            Gene_Annotations
##          WHERE:          gene_symbol LIKE "%<genename>%"
##          ORDER BY        gene_symbol

"""
##      get_gene_annotations_by_gene_id(genename):
"""
##      query_string:       gene_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity
##          FROM            Gene_Annotations
##          WHERE:          gene_id LIKE "%<genename>%"
##          ORDER BY        gene_id

"""
##      get_gene_annotations_by_snp(snpid):
"""
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity
##          FROM            Gene_Annotations
##          WHERE:          snp_id LIKE "%<snpid>%"
##          ORDER BY        snp_id

"""
##      def get_population_by_name(population):
"""
##      query_string:       population_name to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         sample_name, sex, biosample_id, population_code, population_name, superpopulation_code,
##                          superpopulation_name, population_elastic_id, data_collections
##          FROM            Population
##          WHERE:          population_name LIKE "%<population>%"
##          ORDER BY        sample_name

"""
##      def get_population_by_snp(snpid):
"""
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, sample_name, sex, biosample_id, population_code, population_name, superpopulation_code,
##                          population.superpopulation_name AS superpopulation_name, population_elastic_id, data_collections
##          FROM            NP_Associations INNER JOIN Population ON SNP_Associations.population = Population.population_name
##          WHERE:          snp_id LIKE "%<snpid>%"
##          ORDER BY        snp_id

"""
##      def get_snp_and_gene_by_snp(snpid):
"""
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         SNP_Associations.snp_id as snp_associations_snp_id, chromosome, position, p_value, mapped_gene, phenotype, 
##                          population, gene_symbol, gene_id, chromosomal_locus, Gene_Annotations.snp_id as gene_annotations_snp_id, 
##                          pathway, go_term, category, specificity
##          FROM            SNP_Associations LEFT JOIN Gene_Annotations ON SNP_Associations.snp_id = Gene_Annotations.snp_id 
##          WHERE:          SNP_Associations.snp_id LIKE "%<snpid>%"
##          ORDER BY        SNP_Associations.snp_id

"""
##      def get_snp_and_population_by_snp(snpid):
"""
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, sample_name, sex, biosample_id, 
##                          population_code, population_name, superpopulation_code, superpopulation_name, population_elastic_id, data_collections
##          FROM            SNP_Associations LEFT JOIN SNP_Associations.population = Population.population_name
##          WHERE:          snp_id LIKE "%<snpid>%"
##          ORDER BY        snp_id

"""
##      def get_summary_stats_by_population(population):
"""
##      query_string:       population to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         population, tajimas_d, xp_ehh, his, nucleotide_diversity 
##          FROM            Selection_Stats
##          WHERE:          population LIKE "%<population>%"
##          ORDER BY        population

"""
##      def get_summary_stats_by_snp(snpid):
"""
##      query_string:       population to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         Selection_Stats.population AS population, tajimas_d, xp_ehh, his, nucleotide_diversity
##          FROM            SNP_Associations INNER JOIN Selection_Stats ON SNP_Associations.population = Selection_Stats.population
##          WHERE:          snp_id LIKE "%<snpid>%"
##          ORDER BY        snp_id

"""
##      def get_population_stats()
"""
##      return:             dataframe of results (empty if no results)
##          SELECT:         population, tajimas_d, xp_ehh, his, nucleotide_diversity
##          FROM            Selection_Stats
##          ORDER BY        population

"""
##      def get_allele_frequency_by_snp(snpid)
"""
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, FST, population, EAF, MAF
##          FROM            Allele_Frequency
##          WHERE           snp_id LIKE "%<snpid>%"
##          ORDER BY        snp_id

"""
##      def get_fst_by_population(population)
"""
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, FST, population
##          FROM            Allele_Frequency
##          WHERE           population LIKE "%<population>%"
##          ORDER BY        snp_id

"""
##      def get_fst_value_by_snp_for_empty_population(snpid)
"""
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, FST
##          FROM            Allele_Frequency
##          WHERE           snp_id LIKE "%<snpid>%"" AND population IS NULL
##          ORDER BY        snp_id

"""
##      def get_fst_by_snp_and_population(snpid, population, comparisonpopulation)
"""
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, FST, population
##          FROM            Allele_Frequency
##          WHERE           snp_id LIKE "%<snpid>% AND population=="<population>" AND comparison_population=="<comparisonpopulation>"
##          ORDER BY        snp_id


# Import required libraries
import sqlite3
import pandas as pd
from flask import Blueprint, current_app, g

db_api = Blueprint('db_api', __name__)

# Declare database class
class DatabaseClass:
    
    superpopulation = None # Superlopulation name used to partition the database. Allows for expansion to other populations
    SQLlimit = None        # Sets the maximum number of results returned by queries.

    def __init__(self):
        self.dbconnection = None
        
    #
    # Internal Function - Returns a database connection for the current request. If the connection is already established, it will reuse it.
    #
    @staticmethod
    def get_db():
        if 'dbconnection' not in g:
            # Create a new connection for the current request
            database_location = current_app.config['DATABASE_PATH']                         # Get location nof the database
            DatabaseClass.superpopulation = current_app.config['SUPER_POPULATION']          # Get superpopulation name. Allows for future expansion to altertanive populations
            DatabaseClass.SQLlimit = current_app.config['QUERY_LIMIT']                      # Get the SQL query limit
            g.dbconnection = sqlite3.connect(database_location, check_same_thread=False)    # connect to the SQlite database
            g.dbconnection.row_factory = sqlite3.Row                                        # Allow accessing columns by name
        return g.dbconnection


    #
    # Internal Function - Close the database connection at the end of the request.
    #
    @staticmethod
    def close_db():
        dbconnection = getattr(g, 'dbconnection', None)
        if dbconnection is not None:
            dbconnection.close()


    #
    # Query SNP_Associations by ID. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_snp_by_id(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE snp_id LIKE "%{}%" AND superpopulation_name="{}"'
                 'ORDER BY snp_id '
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query SNP_Associations by gene. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_snp_by_gene(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE mapped_gene LIKE "%{}%" AND superpopulation_name="{}"'
                 'ORDER BY snp_id '
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query SNP_Associations by cordinates. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_snp_by_coordinates(chromosome, start, end):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE chromosome = "{}" AND position >= {} AND position <= {} AND superpopulation_name="{}"'
                 'ORDER BY snp_id '
                 'LIMIT {}').format(chromosome, start, end, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df
    
    
    #
    # Query Gene_Annotations by gene symbol. Restricted to global superpopulation. 
    #    
    @staticmethod
    def get_gene_annotations_by_gene_symbol(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE gene_symbol LIKE "%{}%" AND (superpopulation_name="{}" OR superpopulation_name="Global") '
                 'ORDER BY gene_symbol ' 
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query Gene_Annotations by gene id. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_gene_annotations_by_gene_id(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE gene_id LIKE "%{}%" AND (superpopulation_name="{}" OR superpopulation_name="Global") '
                 'ORDER BY gene_id '
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query Gene_Annotations by snpid. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_gene_annotations_by_snp(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE snp_id LIKE "%{}%" AND (superpopulation_name="{}" OR superpopulation_name="Global") '
                 'ORDER BY snp_id '
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df   

    
    #
    # Query Population by name. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_population_by_name(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT sample_name, sex, biosample_id, population_code, population_name, superpopulation_code, '
                 'superpopulation_name, population_elastic_id, data_collections '
                 'FROM Population '
                 'WHERE population_name LIKE "%{}%" AND superpopulation_name="{}"'
                 'ORDER BY sample_name '
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df  

  
    #
    # Query Population by snp_id. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_population_by_snp(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, sample_name, sex, biosample_id, population_code, population_name, superpopulation_code, '
                 'Population.superpopulation_name AS superpopulation_name, population_elastic_id, data_collections '
                 'FROM SNP_Associations INNER JOIN Population ON SNP_Associations.population = Population.population_name '
                 'WHERE snp_id LIKE "%{}%" AND SNP_Associations.superpopulation_name="{}" AND Population.superpopulation_name="{}" '
                 'ORDER BY snp_id '
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df  


    #
    # Query SNP_Associations and Gene_Annotations by snpid. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_snp_and_gene_by_snp(query_string):
        """
        Query SNP_Associations and Gene_Annotations by snpid. Restricted to global superpopulation. First 20 results returned.
        """
        conn = DatabaseClass.get_db()
        query = ('SELECT SNP_Associations.snp_id as snp_associations_snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, '
                 'gene_symbol, gene_id, chromosomal_locus, Gene_Annotations.snp_id as gene_annotations_snp_id, pathway, go_term, category, specificity '
                 'FROM SNP_Associations '
                 'LEFT JOIN Gene_Annotations ON SNP_Associations.snp_id = Gene_Annotations.snp_id '
                 'WHERE SNP_Associations.snp_id LIKE "%{}%" AND SNP_Associations.superpopulation_name="{}" AND (Gene_Annotations.superpopulation_name="{}" OR Gene_Annotations.superpopulation_name="Global")'
                 'ORDER BY SNP_Associations.snp_id ' 
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df

    
    # 
    # Query SNP_Associations Population and by snpid. Restricted to global superpopulation. 
    #    
    @staticmethod
    def get_snp_and_population_by_snp(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, sample_name, sex, biosample_id '
                 'population_code, population_name, superpopulation_code, Population.superpopulation_name AS superpopulation_name, population_elastic_id, data_collections '
                 'FROM SNP_Associations '
                 'LEFT JOIN Population ON SNP_Associations.population = Population.population_name '
                 'WHERE snp_id LIKE "%{}%" AND SNP_Associations.superpopulation_name="{}" AND Population.superpopulation_name="{}" '
                 'ORDER BY snp_id ' 
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query Selection_Stats by population name. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_summary_stats_by_population(query_string):

        conn = DatabaseClass.get_db()
        query = ('SELECT population, tajimas_d, xp_ehh, his, nucleotide_diversity '
                 'FROM Selection_Stats '
                 'WHERE population LIKE "%{}%" AND superpopulation_name="{}"'
                 'ORDER BY population ' 
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df

    
    #
    # Query population Stats. Restricted to global superpopulation. 
    #    
    @staticmethod
    def get_population_stats():
        conn = db.get_db()
        query = ('SELECT population, tajimas_d, xp_ehh, his, nucleotide_diversity '
             'FROM Selection_Stats '
             'WHERE superpopulation_name="{}"'
             'ORDER BY population ' 
             'LIMIT {}').format(DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query SNP_Associations and Selection_Stats by snpid. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_summary_stats_by_snp(query_string):

        conn = DatabaseClass.get_db()
        query = ('SELECT SNP_Associations.snp_id AS snp_id, Selection_Stats.population AS population, tajimas_d, xp_ehh, his, nucleotide_diversity '
                 'FROM SNP_Associations '
                 'LEFT JOIN Selection_Stats ON SNP_Associations.population = Selection_Stats.population '
                 'WHERE snp_id LIKE "%{}%" AND SNP_Associations.superpopulation_name="{}" AND Selection_Stats.superpopulation_name="{}" '
                 'ORDER BY snp_id ' 
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query Allele_Frequency by snpid. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_allele_frequency_by_snp(query_string):

        conn = DatabaseClass.get_db()
        query = ('SELECT  snp_id, FST, population, EAF, MAF '
                 'FROM Allele_Frequency '
                 'WHERE snp_id LIKE "%{}%" AND superpopulation_name="{}" '
                 'ORDER BY snp_id ' 
                 'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query Allele_Frequency by population. Restricted to global superpopulation. 
    #
    @staticmethod
    def get_fst_by_population(query_string):

        conn = DatabaseClass.get_db()
        populationquery = 'population IS NULL' if query_string=='' else 'population="{}"'.format(query_string)
        query = ('SELECT  snp_id, FST, population '
                 'FROM Allele_Frequency '
                 'WHERE ' + populationquery + ' AND superpopulation_name="{}" '
                 'ORDER BY snp_id ' 
                 'LIMIT {}').format(DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df


    #
    # Query Allele_Frequency by snp. Restricted to global superpopulation. 
    #    
    @staticmethod
    def get_fst_value_by_snp_for_empty_population(query_string):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, FST '
             'FROM Allele_Frequency '
             'WHERE snp_id LIKE "%{}%" AND (population = "" OR population IS NULL) AND superpopulation_name="{}" '
             'ORDER BY snp_id '
             'LIMIT {}').format(query_string, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        df['FST'] = df['FST'].round(3)  # Round to 3dp for screen presentation
        return df


    #
    # Query Allele_Frequency by snp and population. Restricted to Northern Europeans from Utah Comparison_population. 
    # 
    @staticmethod
    def get_fst_by_snp_and_population(snp_id, population, comparisonpopulation):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, FST, population '
                 'FROM Allele_Frequency '
                 'WHERE snp_id LIKE "%{}%" '
                 'AND population = "{}" AND comparison_population = "{}" AND superpopulation_name="{}" '
                 'ORDER BY snp_id '
                 'LIMIT {}').format(snp_id, population, comparisonpopulation, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df
    
    #
    # Query Allele_Frequency by snp and population. Restricted to Northern Europeans from Utah Comparison_population. 
    # 
    @staticmethod
    def get_stats_by_snp_and_population(snp_id, population, comparisonpopulation):
        conn = DatabaseClass.get_db()
        query = ('SELECT snp_id, FST, population, NSL '
                 'FROM Allele_Frequency_WITH_NSL '
                 'WHERE snp_id LIKE "%{}%" '
                 'AND population = "{}" AND comparison_population = "{}" AND superpopulation_name="{}" '
                 'ORDER BY snp_id '
                 'LIMIT {}').format(snp_id, population, comparisonpopulation, DatabaseClass.superpopulation, DatabaseClass.SQLlimit)
        df = pd.read_sql_query(query, conn)
        return df



#
# Internal Function - After using g.dbconnection, close it after the request lifecycle ends:
#
def close_app_connection(exception=None):
    dbconnection = getattr(g, 'dbconnection', None)
    if dbconnection is not None:
        dbconnection.close()


#
# Internal Function - Bind the close_app_connection function to be executed after each request
#
from flask import current_app

def init_db_teardown(app):
    @app.teardown_request
    def close_connection(exception=None):
        close_app_connection(exception)

# publish class
db = DatabaseClass()

