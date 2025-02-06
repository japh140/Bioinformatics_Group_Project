##
## DATABASE API
##

##
## db_open():
##      Open connection to the database
##
##
## db_close():
##      Close connection to the database
##
##
## get_snp_by_id(query_string):
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population
##          FROM            SNP_Associations
##          WHERE:          snp_id LIKE "%<query_string>%""
##          ORDER BY        snp_id
##          LIMIT           20
##
##
## get_snp_by_gene(query_string):
##      query_string:       mapped_gene to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population
##          FROM            SNP_Associations
##          WHERE:          mapped_gene LIKE "%<query_string>%""
##          ORDER BY        snp_id
##          LIMIT           20
##
##
## get_snp_by_coordinates(chromosome, start, end):
##      chromosome:         snp_chromosomeid to query
##      start               starting chromosome position to query from
##      end                 ending chromosome position to query to
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population
##          FROM            SNP_Associations
##          WHERE:          WHERE chromosome = "<chromosome>" AND position >= <start> AND position <= <end>
##          ORDER BY        snp_id
##          LIMIT           20
##
## get_gene_annotations_by_gene_symbol(query_string):
##      query_string:       gene_symbol to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity
##          FROM            Gene_Annotations
##          WHERE:          gene_symbol LIKE "%<query_string>%""
##          ORDER BY        gene_symbol
##          LIMIT           20
##
##
## get_gene_annotations_by_gene_id(query_string):
##      query_string:       gene_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity
##          FROM            Gene_Annotations
##          WHERE:          gene_id LIKE "%<query_string>%""
##          ORDER BY        gene_id
##          LIMIT           20
##
##
## get_gene_annotations_by_snp(query_string):
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity
##          FROM            Gene_Annotations
##          WHERE:          snp_id LIKE "%<query_string>%""
##          ORDER BY        snp_id
##          LIMIT           20
##
##
## def get_population_by_name(query_string):
##      query_string:       population_name to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         sample_name, sex, biosample_id, population_code, population_name, superpopulation_code,
##                          superpopulation_name, population_elastic_id, data_collections
##          FROM            Population
##          WHERE:          population_name LIKE "%<query_string>%""
##          ORDER BY        sample_name
##          LIMIT           20
##
##
## def get_snp_and_gene_by_snp(query_string):
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         SNP_Associations.snp_id as snp_associations_snp_id, chromosome, position, p_value, mapped_gene, phenotype, 
##                          population, gene_symbol, gene_id, chromosomal_locus, Gene_Annotations.snp_id as gene_annotations_snp_id, 
##                          pathway, go_term, category, specificity
##          FROM            SNP_Associations LEFT JOIN Gene_Annotations ON SNP_Associations.snp_id = Gene_Annotations.snp_id 
##          WHERE:          SNP_Associations.snp_id LIKE "%<query_string>%""
##          ORDER BY        SNP_Associations.snp_id
##          LIMIT           20
##
##
## def get_snp_and_population_by_snp(query_string):
##      query_string:       snp_id to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, sample_name, sex, biosample_id, 
##                          population_code, population_name, superpopulation_code, superpopulation_name, population_elastic_id, data_collections
##          FROM            SNP_Associations LEFT JOIN SNP_Associations.population = Population.population_name
##          WHERE:          snp_id LIKE "%<query_string>%""
##          ORDER BY        snp_id
##          LIMIT           20
##
##
## def get_summary_stats_by_population(query_string):
##      query_string:       population to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         population, tajimas_d, xp_ehh, his, nucleotide_diversity 
##          FROM            Selection_Stats
##          WHERE:          population LIKE "%<query_string>%""
##          ORDER BY        population
##          LIMIT           20
##
##
## def get_summary_stats_by_snp(query_string):
##      query_string:       population to query
##      return:             dataframe of results (empty if no results)
##          SELECT:         Selection_Stats.population AS population, tajimas_d, xp_ehh, his, nucleotide_diversity
##          FROM            SNP_Associations INNER JOIN Selection_Stats ON SNP_Associations.population = Selection_Stats.population
##          WHERE:          snp_id LIKE "%<query_string>%""
##          ORDER BY        snp_id
##          LIMIT           20
##


import sqlite3
import pandas as pd
from flask import Blueprint, current_app, g

db_api = Blueprint('db_api', __name__)

class DatabaseClass:
    def __init__(self):
        self.dbconnection = None

    @staticmethod
    def get_db():
        """
        Returns a database connection for the current request.
        If the connection is already established, it will reuse it.
        """
        if 'dbconnection' not in g:
            # Create a new connection for the current request
            database_location = current_app.config['DATABASE_PATH']
            g.dbconnection = sqlite3.connect(database_location, check_same_thread=False)
            g.dbconnection.row_factory = sqlite3.Row  # Allow accessing columns by name
        return g.dbconnection

    @staticmethod
    def close_db():
        """
        Close the database connection at the end of the request.
        """
        dbconnection = getattr(g, 'dbconnection', None)
        if dbconnection is not None:
            dbconnection.close()

    @staticmethod
    def get_snp_by_id(query_string):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE snp_id LIKE "%{}%" '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_snp_by_gene(query_string):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE mapped_gene LIKE "%{}%" '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_snp_by_coordinates(chromosome, start, end):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE chromosome = "{}" AND position >= {} AND position <= {} '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(chromosome, start, end)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df
    
    @staticmethod
    def get_gene_annotations_by_gene_symbol(query_string):
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE gene_symbol LIKE "%{}%" ' 
                 'ORDER BY gene_symbol ' 
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_gene_annotations_by_gene_id(query_string):
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE gene_id LIKE "%{}%" '
                 'ORDER BY gene_id '
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_gene_annotations_by_snp(query_string):
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE snp_id LIKE "%{}%" '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df   

    @staticmethod
    def get_population_by_name(query_string):
        query = ('SELECT sample_name, sex, biosample_id, population_code, population_name, superpopulation_code, '
                 'superpopulation_name, population_elastic_id, data_collections '
                 'FROM Population '
                 'WHERE population_name LIKE "%{}%" '
                 'ORDER BY sample_name '
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df  

    @staticmethod
    def get_snp_and_gene_by_snp(query_string):
        query = ('SELECT SNP_Associations.snp_id as snp_associations_snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, '
                 'gene_symbol, gene_id, chromosomal_locus, Gene_Annotations.snp_id as gene_annotations_snp_id, pathway, go_term, category, specificity '
                 'FROM SNP_Associations '
                 'LEFT JOIN Gene_Annotations ON SNP_Associations.snp_id = Gene_Annotations.snp_id '
                 'WHERE SNP_Associations.snp_id LIKE "%{}%" '
                 'ORDER BY SNP_Associations.snp_id ' 
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_snp_and_population_by_snp(query_string):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population, sample_name, sex, biosample_id '
                 'population_code, population_name, superpopulation_code, superpopulation_name, population_elastic_id, data_collections '
                 'FROM SNP_Associations '
                 'LEFT JOIN Population ON SNP_Associations.population = Population.population_name '
                 'WHERE snp_id LIKE "%{}%" '
                 'ORDER BY snp_id ' 
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_summary_stats_by_population(query_string):
        query = ('SELECT population, tajimas_d, xp_ehh, his, nucleotide_diversity '
                 'FROM Selection_Stats '
                 'WHERE population LIKE "%{}%" '
                 'ORDER BY population ' 
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df

    @staticmethod
    def get_summary_stats_by_snp(query_string):
        query = ('SELECT Selection_Stats.population AS population, tajimas_d, xp_ehh, his, nucleotide_diversity '
                 'FROM SNP_Associations '
                 'INNER JOIN Selection_Stats ON SNP_Associations.population = Selection_Stats.population '
                 'WHERE snp_id LIKE "%{}%" '
                 'ORDER BY snp_id ' 
                 'LIMIT 20').format(query_string)
        
        conn = DatabaseClass.get_db()
        df = pd.read_sql_query(query, conn)
        return df


# After using g.dbconnection, don't forget to close it after the request lifecycle ends:
def close_app_connection(exception=None):
    dbconnection = getattr(g, 'dbconnection', None)
    if dbconnection is not None:
        dbconnection.close()

# Bind the close_app_connection function to be executed after each request
from flask import current_app

def init_db_teardown(app):
    @app.teardown_request
    def close_connection(exception=None):
        close_app_connection(exception)


db = DatabaseClass()

