from flask import Flask
from app.config import Config

try:
    # try absolute path first
    from app.blueprints.db_api.db_api import db_api, init_db_teardown, db
except ImportError:
    # fall back to relative path
    from blueprints.db_api.db_api import db_api, init_db_teardown, db

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(db_api)
app.app_context().push()
init_db_teardown(app)

#
# Test get_snp_by_id()
#
print('\n\033[94m TESTING: get_snp_by_id() \033[0m')
df = db.get_snp_by_id('rs123')
print(df)
assert len(df)==5,                   "\033[91m Error1 : get_snp_by_id() \033[0m"
assert len(df.columns)==7,           "\033[91m Error2 : get_snp_by_id() \033[0m"
assert df.columns[0]=='snp_id',      "\033[91m Error3 : get_snp_by_id() \033[0m"
assert df.columns[1]=='chromosome',  "\033[91m Error4 : get_snp_by_id() \033[0m"
assert df.columns[2]=='position',    "\033[91m Error5 : get_snp_by_id() \033[0m"
assert df.columns[3]=='p_value',     "\033[91m Error6 : get_snp_by_id() \033[0m"
assert df.columns[4]=='mapped_gene', "\033[91m Error7 : get_snp_by_id() \033[0m"
assert df.columns[5]=='phenotype',   "\033[91m Error8 : get_snp_by_id() \033[0m"
assert df.columns[6]=='population',  "\033[91m Error9 : get_snp_by_id() \033[0m"

df = db.get_snp_by_id('Gaijn@#_+')
print(df)
assert len(df)==0,                   "\033[91m Error10 : get_snp_by_id() \033[0m"
assert len(df.columns)==7,           "\033[91m Error11 : get_snp_by_id() \033[0m"

#
# Test get_snp_by_gene
#
print('\n\033[94m TESTING: get_snp_by_gene \033[0m')
df = db.get_snp_by_gene('KCNQ1')
print(df)
assert len(df)==25,                  "\033[91m Error1 : get_snp_by_gene \033[0m"
assert len(df.columns)==7,           "\033[91m Error2 : get_snp_by_gene \033[0m"
assert df.columns[0]=='snp_id',      "\033[91m Error3 : get_snp_by_gene \033[0m"
assert df.columns[1]=='chromosome',  "\033[91m Error4 : get_snp_by_gene \033[0m"
assert df.columns[2]=='position',    "\033[91m Error5 : get_snp_by_gene \033[0m"
assert df.columns[3]=='p_value',     "\033[91m Error6 : get_snp_by_gene \033[0m"
assert df.columns[4]=='mapped_gene', "\033[91m Error7 : get_snp_by_gene \033[0m"
assert df.columns[5]=='phenotype',   "\033[91m Error8 : get_snp_by_gene \033[0m"
assert df.columns[6]=='population',  "\033[91m Error9 : get_snp_by_gene \033[0m"

df = db.get_snp_by_gene('Gaijn@#_+')
print(df)
assert len(df)==0,                   "\033[91m Error10 : get_snp_by_gene \033[0m"
assert len(df.columns)==7,           "\033[91m Error11 : get_snp_by_gene \033[0m"

#
# Test get_snp_by_coordinates
#
print('\n\033[94m TESTING: get_snp_by_coordinates \033[0m')
df = db.get_snp_by_coordinates('11', 2500000, 2700000)
print(df)
assert len(df)==16,                   "\033[91m Error1 : get_snp_by_coordinates \033[0m"
assert len(df.columns)==7,           "\033[91m Error2 : get_snp_by_coordinates \033[0m"
assert df.columns[0]=='snp_id',      "\033[91m Error3 : get_snp_by_coordinates \033[0m"
assert df.columns[1]=='chromosome',  "\033[91m Error4 : get_snp_by_coordinates \033[0m"
assert df.columns[2]=='position',    "\033[91m Error5 : get_snp_by_coordinates \033[0m"
assert df.columns[3]=='p_value',     "\033[91m Error6 : get_snp_by_coordinates \033[0m"
assert df.columns[4]=='mapped_gene', "\033[91m Error7 : get_snp_by_coordinates \033[0m"
assert df.columns[5]=='phenotype',   "\033[91m Error8 : get_snp_by_coordinates \033[0m"
assert df.columns[6]=='population',  "\033[91m Error9 : get_snp_by_coordinates \033[0m"

df = db.get_snp_by_id('Gaijn@#_+')
print(df)
assert len(df)==0,                   "\033[91m Error10 : get_snp_by_coordinates \033[0m"
assert len(df.columns)==7,           "\033[91m Error11 : get_snp_by_coordinates \033[0m"

#
# Test get_gene_annotations_by_gene_symbol
#
print('\n\033[94m TESTING: get_gene_annotations_by_gene_symbol \033[0m')
df = db.get_gene_annotations_by_gene_symbol('MTNR1B')
print(df)
assert len(df)==2,                          "\033[91m Error1 : get_gene_annotations_by_gene_symbol \033[0m"
assert len(df.columns)==8,                  "\033[91m Error2 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[0]=='gene_symbol',        "\033[91m Error3 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[1]=='gene_id',            "\033[91m Error4 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[2]=='chromosomal_locus',  "\033[91m Error5 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[3]=='snp_id',             "\033[91m Error6 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[4]=='pathway',            "\033[91m Error7 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[5]=='go_term',            "\033[91m Error8 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[6]=='category',           "\033[91m Error9 : get_gene_annotations_by_gene_symbol \033[0m"
assert df.columns[7]=='specificity',        "\033[91m Error10 : get_gene_annotations_by_gene_symbol \033[0m"

df = db.get_gene_annotations_by_gene_symbol('Gaijn@#_+')
print(df)
assert len(df)==0,                          "\033[91m Error11 : get_gene_annotations_by_gene_symbol \033[0m"
assert len(df.columns)==8,                  "\033[91m Error12 : get_gene_annotations_by_gene_symbol \033[0m"

#
# Test get_gene_annotations_by_gene_id
#
print('\n\033[94m TESTING: get_gene_annotations_by_gene_id \033[0m')
df = db.get_gene_annotations_by_gene_id('6934')
print(df)
assert len(df)==4,                          "\033[91m Error1 : get_gene_annotations_by_gene_id \033[0m"
assert len(df.columns)==8,                  "\033[91m Error2 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[0]=='gene_symbol',        "\033[91m Error3 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[1]=='gene_id',            "\033[91m Error4 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[2]=='chromosomal_locus',  "\033[91m Error5 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[3]=='snp_id',             "\033[91m Error6 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[4]=='pathway',            "\033[91m Error7 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[5]=='go_term',            "\033[91m Error8 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[6]=='category',           "\033[91m Error9 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[7]=='specificity',        "\033[91m Error10 : get_gene_annotations_by_gene_id \033[0m"

df = db.get_gene_annotations_by_gene_symbol('Gaijn@#_+')
print(df)
assert len(df)==0,                          "\033[91m Error11 : get_gene_annotations_by_gene_id \033[0m"
assert len(df.columns)==8,                  "\033[91m Error12 : get_gene_annotations_by_gene_id \033[0m"

#
# Test get_gene_annotations_by_gene_id
#
print('\n\033[94m TESTING: get_gene_annotations_by_snp \033[0m')
df = db.get_gene_annotations_by_snp('rs1801282')
print(df)
assert len(df)==2,                          "\033[91m Error1 : get_gene_annotations_by_snp \033[0m"
assert len(df.columns)==8,                  "\033[91m Error2 : get_gene_annotations_by_snp \033[0m"
assert df.columns[0]=='gene_symbol',        "\033[91m Error3 : get_gene_annotations_by_snp \033[0m"
assert df.columns[1]=='gene_id',            "\033[91m Error4 : get_gene_annotations_by_snp \033[0m"
assert df.columns[2]=='chromosomal_locus',  "\033[91m Error5 : get_gene_annotations_by_snp \033[0m"
assert df.columns[3]=='snp_id',             "\033[91m Error6 : get_gene_annotations_by_snp \033[0m"
assert df.columns[4]=='pathway',            "\033[91m Error7 : get_gene_annotations_by_snp \033[0m"
assert df.columns[5]=='go_term',            "\033[91m Error8 : get_gene_annotations_by_snp \033[0m"
assert df.columns[6]=='category',           "\033[91m Error9 : get_gene_annotations_by_snp \033[0m"
assert df.columns[7]=='specificity',        "\033[91m Error10 : get_gene_annotations_by_snp \033[0m"

df = db.get_gene_annotations_by_gene_symbol('Gaijn@#_+')
print(df)
assert len(df)==0,                          "\033[91m Error11 : get_gene_annotations_by_snp \033[0m"
assert len(df.columns)==8,                  "\033[91m Error12 : get_gene_annotations_by_snp \033[0m"


#
# Test get_snp_and_gene_by_snp
#
print('\n\033[94m TESTING: get_snp_and_gene_by_snp \033[0m')
df = db.get_snp_and_gene_by_snp('rs5219')
print(df)
assert len(df)==2,                                  "\033[91m Error1 : get_snp_and_gene_by_snp \033[0m"
assert len(df.columns)==15,                         "\033[91m Error2 : get_snp_and_gene_by_snp \033[0m"
assert df.columns[ 0]=='snp_associations_snp_id',   "\033[91m Error3 : get_snp_and_gene_by_snp \033[0m"
assert df.columns[ 1]=='chromosome',                "\033[91m Error4 : get_snp_by_coordinates \033[0m"
assert df.columns[ 2]=='position',                  "\033[91m Error5 : get_snp_by_coordinates \033[0m"
assert df.columns[ 3]=='p_value',                   "\033[91m Error6 : get_snp_by_coordinates \033[0m"
assert df.columns[ 4]=='mapped_gene',               "\033[91m Error7 : get_snp_by_coordinates \033[0m"
assert df.columns[ 5]=='phenotype',                 "\033[91m Error8 : get_snp_by_coordinates \033[0m"
assert df.columns[ 6]=='population',                "\033[91m Error9 : get_snp_by_coordinates \033[0m"
assert df.columns[ 7]=='gene_symbol',               "\033[91m Error10 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[ 8]=='gene_id',                   "\033[91m Error11 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[ 9]=='chromosomal_locus',         "\033[91m Error12 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[10]=='gene_annotations_snp_id',   "\033[91m Error13 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[11]=='pathway',                   "\033[91m Error14 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[12]=='go_term',                   "\033[91m Error15 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[13]=='category',                  "\033[91m Error16 : get_gene_annotations_by_gene_id \033[0m"
assert df.columns[14]=='specificity',               "\033[91m Error17 : get_gene_annotations_by_gene_id \033[0m"
assert df['specificity'].iloc[0]!=''

df = db.get_snp_and_gene_by_snp('Gaijn@#_+')
print(df)
assert len(df)==0,                                  "\033[91m Error18 : get_snp_and_gene_by_snp \033[0m"
assert len(df.columns)==15,                         "\033[91m Error19 : get_snp_and_gene_by_snp \033[0m"


#
# Test get_allele_frequency_by_snp
#
print('\n\033[94m TESTING: get_allele_frequency_by_snp \033[0m')
df = db.get_allele_frequency_by_snp('rs12219514')
print(df)
assert len(df)==4,                              "\033[91m Error1 : get_allele_frequency_by_snp \033[0m"
assert len(df.columns)==5,                      "\033[91m Error2 : get_allele_frequency_by_snp \033[0m"
assert df.columns[0]=='snp_id',                 "\033[91m Error3 : get_allele_frequency_by_snp \033[0m"
assert df.columns[1]=='FST',                    "\033[91m Error4 : get_allele_frequency_by_snp \033[0m"
assert df.columns[2]=='population',             "\033[91m Error5 : get_allele_frequency_by_snp \033[0m"
assert df.columns[3]=='EAF',                    "\033[91m Error6 : get_allele_frequency_by_snp \033[0m"
assert df.columns[4]=='MAF',                    "\033[91m Error7 : get_allele_frequency_by_snp \033[0m"

df = db.get_allele_frequency_by_snp('Gaijn@#_+')
print(df)
assert len(df)==0,                              "\033[91m Error8 : get_allele_frequency_by_snp \033[0m"
assert len(df.columns)==5,                      "\033[91m Error9 : get_allele_frequency_by_snp \033[0m"


#
# Test get_fst_by_population
#
print('\n\033[94m TESTING: get_fst_by_population \033[0m')
df = db.get_fst_by_population('Punjabi')
print(df)
assert len(df)==25,                             "\033[91m Error1 : get_fst_by_population \033[0m"
assert len(df.columns)==3,                      "\033[91m Error2 : get_fst_by_population \033[0m"
assert df.columns[0]=='snp_id',                 "\033[91m Error3 : get_fst_by_population \033[0m"
assert df.columns[1]=='FST',                    "\033[91m Error4 : get_fst_by_population \033[0m"
assert df.columns[2]=='population',             "\033[91m Error5 : get_fst_by_population \033[0m"

df = db.get_fst_by_population('')
print(df)
assert len(df)==25,                             "\033[91m Error6 : get_fst_by_population \033[0m"
assert len(df.columns)==3,                      "\033[91m Error7 : get_fst_by_population \033[0m"
assert df.columns[0]=='snp_id',                 "\033[91m Error8 : get_fst_by_population \033[0m"
assert df.columns[1]=='FST',                    "\033[91m Error9 : get_fst_by_population \033[0m"
assert df.columns[2]=='population',             "\033[91m Error10 : get_fst_by_population \033[0m"

df = db.get_fst_by_population('Gaijn@#_+')
print(df)
assert len(df)==0,                             "\033[91m Error11 : get_fst_by_population \033[0m"
assert len(df.columns)==3,                     "\033[91m Error12 : get_fst_by_population \033[0m"


#
# Test get_fst_value_by_snp_for_empty_population
#
print('\n\033[94m TESTING: get_fst_value_by_snp_for_empty_population \033[0m')
df = db.get_fst_value_by_snp_for_empty_population('rs7903146')
print(df)
assert len(df)==1,                              "\033[91m Error1 : get_fst_value_by_snp_for_empty_population \033[0m"
assert len(df.columns)==2,                      "\033[91m Error2 : get_fst_value_by_snp_for_empty_population \033[0m"
assert df.columns[0]=='snp_id',                 "\033[91m Error3 : get_fst_value_by_snp_for_empty_population \033[0m"
assert df.columns[1]=='FST',                    "\033[91m Error4 : get_fst_value_by_snp_for_empty_population \033[0m"

df = db.get_fst_value_by_snp_for_empty_population('Gaijn@#_+')
print(df)
assert len(df)==0,                             "\033[91m Error6 : get_fst_value_by_snp_for_empty_population \033[0m"
assert len(df.columns)==2,                     "\033[91m Error6 : get_fst_value_by_snp_for_empty_population \033[0m"


#
# Test get_stats_by_snp_and_population
#
print('\n\033[94m TESTING: get_stats_by_snp_and_population \033[0m')
df = db.get_stats_by_snp_and_population('rs7903146','Bengali','Northern Europeans from Utah')
print(df)
assert len(df)==1,                              "\033[91m Error1 : get_stats_by_snp_and_population \033[0m"
assert len(df.columns)==4,                      "\033[91m Error2 : get_stats_by_snp_and_population \033[0m"
assert df.columns[0]=='snp_id',                 "\033[91m Error3 : get_stats_by_snp_and_population \033[0m"
assert df.columns[1]=='FST',                    "\033[91m Error4 : get_stats_by_snp_and_population \033[0m"
assert df.columns[2]=='population',             "\033[91m Error5 : get_stats_by_snp_and_population \033[0m"
assert df.columns[3]=='NSL',                    "\033[91m Error6 : get_stats_by_snp_and_population \033[0m"

df = db.get_stats_by_snp_and_population('Gaijn@#_+','Bengali','Northern Europeans from Utah')
print(df)
assert len(df)==0,                             "\033[91m Error7 : get_stats_by_snp_and_population \033[0m"
assert len(df.columns)==4,                     "\033[91m Error7 : get_stats_by_snp_and_population \033[0m"


#
# All OK
#
print ('\n\033[92m EVERYTHING IS WORKING \033[0m')