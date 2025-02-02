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
    def get_gene_annotations_by_gene_symbol(querystring):
        query = 'SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity ' \
        + 'FROM Gene_Annotations ' \
        + 'WHERE gene_symbol LIKE ' + '"%' + querystring + '%" ' \
        + 'ORDER BY gene_symbol ' \
        + 'LIMIT 20'
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df

    @staticmethod
    def get_gene_annotations_by_gene_id(querystring):
        query = 'SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity ' \
        + 'FROM Gene_Annotations ' \
        + 'WHERE gene_id LIKE ' + '"%' + querystring + '%" ' \
        + 'ORDER BY gene_id ' \
        + 'LIMIT 20'
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df

    @staticmethod
    def get_gene_annotations_by_snp(querystring):
        query = 'SELECT gene_symbol, gene_id, chromosomal_locus, snp_id, pathway, go_term, category, specificity ' \
        + 'FROM Gene_Annotations ' \
        + 'WHERE snp_id LIKE ' + '"%' + querystring + '%" ' \
        + 'ORDER BY snp_id ' \
        + 'LIMIT 20'
        print(query)
        df = pd.read_sql_query(query,db.dbconnection)
        return df   

db = DatabaseClass()