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

import sqlite3
import pandas as pd
from flask import Blueprint, current_app

db_api = Blueprint('db_api', __name__)

class DatabaseClass:
    def __init__(self):
        self.dbconnection = None

    @staticmethod
    def db_open():
        database_location = current_app.config['DATABASE_PATH']
        db.dbconnection = sqlite3.connect(database_location)

    @staticmethod
    def db_close():
        db.dbconnection.close()

    @staticmethod
    def get_snp_by_id(query_string):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE snp_id LIKE "%{}%" '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(query_string)
        print(query)
        df = pd.read_sql_query(query, db.dbconnection)
        return df

    @staticmethod
    def get_snp_by_gene(query_string):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE mapped_gene LIKE "%{}%" '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(query_string)
        print(query)
        df = pd.read_sql_query(query, db.dbconnection)
        return df

    @staticmethod
    def get_snp_by_coordinates(chromosome, start, end):
        query = ('SELECT snp_id, chromosome, position, p_value, mapped_gene, phenotype, population '
                 'FROM SNP_Associations '
                 'WHERE chromosome = "{}" AND position >= {} AND position <= {} '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(chromosome, start, end)
        print(query)
        df = pd.read_sql_query(query, db.dbconnection)
        return df
    
    @staticmethod
    def get_gene_annotations_by_gene_symbol(query_string):
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE gene_symbol LIKE "%{}%" ' 
                 'ORDER BY gene_symbol ' 
                 'LIMIT 20').format(query_string)
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df

    @staticmethod
    def get_gene_annotations_by_gene_id(query_string):
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE gene_id LIKE "%{}%" '
                 'ORDER BY gene_id '
                 'LIMIT 20').format(query_string)
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df

    @staticmethod
    def get_gene_annotations_by_snp(query_string):
        query = ('SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity '
                 'FROM Gene_Annotations '
                 'WHERE snp_id LIKE "%{}%" '
                 'ORDER BY snp_id '
                 'LIMIT 20').format(query_string)
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df   

    @staticmethod
    def get_population_by_name(query_string):
        query = ('SELECT sample_name, sex, biosample_id, population_code, population_name, superpopulation_code, '
                 'superpopulation_name, population_elastic_id, data_collections '
                 'FROM Population '
                 'WHERE population_name LIKE "%{}%" '
                 'ORDER BY sample_name '
                 'LIMIT 20').format(query_string)
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
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
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
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
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df


db = DatabaseClass()