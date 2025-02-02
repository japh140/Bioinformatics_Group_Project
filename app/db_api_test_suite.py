from blueprints.db_api.db_api import DatabaseClass

#
# Open Database Connection
#
DatabaseClass.db_open()

#
# Test get_snp_by_id()
#
print('\n\033[94m TESTING: get_snp_by_id() \033[0m')
df = DatabaseClass.get_snp_by_id('rs123')
print(df)
assert len(df)==3,                   "\033[91m Error1 : get_snp_by_id() \033[0m"
assert len(df.columns)==7,           "\033[91m Error2 : get_snp_by_id() \033[0m"
assert df.columns[0]=='snp_id',      "\033[91m Error3 : get_snp_by_id() \033[0m"
assert df.columns[1]=='chromosome',  "\033[91m Error4 : get_snp_by_id() \033[0m"
assert df.columns[2]=='position',    "\033[91m Error5 : get_snp_by_id() \033[0m"
assert df.columns[3]=='p_value',     "\033[91m Error6 : get_snp_by_id() \033[0m"
assert df.columns[4]=='mapped_gene', "\033[91m Error7 : get_snp_by_id() \033[0m"
assert df.columns[5]=='phenotype',   "\033[91m Error8 : get_snp_by_id() \033[0m"
assert df.columns[6]=='population',  "\033[91m Error9 : get_snp_by_id() \033[0m"

df = DatabaseClass.get_snp_by_id('Gaijn@#_+')
print(df)
assert len(df)==0,                   "\033[91m Error10 : get_snp_by_id() \033[0m"
assert len(df.columns)==7,           "\033[91m Error11 : get_snp_by_id() \033[0m"

#
# Test get_snp_by_gene
#
print('\n\033[94m TESTING: get_snp_by_gene \033[0m')
df = DatabaseClass.get_snp_by_gene('KCNQ1')
print(df)
assert len(df)==20,                  "\033[91m Error1 : get_snp_by_gene \033[0m"
assert len(df.columns)==7,           "\033[91m Error2 : get_snp_by_gene \033[0m"
assert df.columns[0]=='snp_id',      "\033[91m Error3 : get_snp_by_gene \033[0m"
assert df.columns[1]=='chromosome',  "\033[91m Error4 : get_snp_by_gene \033[0m"
assert df.columns[2]=='position',    "\033[91m Error5 : get_snp_by_gene \033[0m"
assert df.columns[3]=='p_value',     "\033[91m Error6 : get_snp_by_gene \033[0m"
assert df.columns[4]=='mapped_gene', "\033[91m Error7 : get_snp_by_gene \033[0m"
assert df.columns[5]=='phenotype',   "\033[91m Error8 : get_snp_by_gene \033[0m"
assert df.columns[6]=='population',  "\033[91m Error9 : get_snp_by_gene \033[0m"

df = DatabaseClass.get_snp_by_gene('Gaijn@#_+')
print(df)
assert len(df)==0,                   "\033[91m Error10 : get_snp_by_gene \033[0m"
assert len(df.columns)==7,           "\033[91m Error11 : get_snp_by_gene \033[0m"

#
# Test get_snp_by_coordinates
#
print('\n\033[94m TESTING: get_snp_by_coordinates \033[0m')
df = DatabaseClass.get_snp_by_coordinates('11', 2500000, 2700000)
print(df)
assert len(df)==9,                   "\033[91m Error1 : get_snp_by_coordinates \033[0m"
assert len(df.columns)==7,           "\033[91m Error2 : get_snp_by_coordinates \033[0m"
assert df.columns[0]=='snp_id',      "\033[91m Error3 : get_snp_by_coordinates \033[0m"
assert df.columns[1]=='chromosome',  "\033[91m Error4 : get_snp_by_coordinates \033[0m"
assert df.columns[2]=='position',    "\033[91m Error5 : get_snp_by_coordinates \033[0m"
assert df.columns[3]=='p_value',     "\033[91m Error6 : get_snp_by_coordinates \033[0m"
assert df.columns[4]=='mapped_gene', "\033[91m Error7 : get_snp_by_coordinates \033[0m"
assert df.columns[5]=='phenotype',   "\033[91m Error8 : get_snp_by_coordinates \033[0m"
assert df.columns[6]=='population',  "\033[91m Error9 : get_snp_by_coordinates \033[0m"

df = DatabaseClass.get_snp_by_id('Gaijn@#_+')
print(df)
assert len(df)==0,                   "\033[91m Error10 : get_snp_by_coordinates \033[0m"
assert len(df.columns)==7,           "\033[91m Error11 : get_snp_by_coordinates \033[0m"

#
# Test get_gene_annotations_by_gene_symbol
#
print('\n\033[94m TESTING: get_gene_annotations_by_gene_symbol \033[0m')
df = DatabaseClass.get_gene_annotations_by_gene_symbol('MTNR1B')
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

df = DatabaseClass.get_gene_annotations_by_gene_symbol('Gaijn@#_+')
print(df)
assert len(df)==0,                          "\033[91m Error11 : get_gene_annotations_by_gene_symbol \033[0m"
assert len(df.columns)==8,                  "\033[91m Error12 : get_gene_annotations_by_gene_symbol \033[0m"

#
# Test get_gene_annotations_by_gene_id
#
print('\n\033[94m TESTING: get_gene_annotations_by_gene_id \033[0m')
df = DatabaseClass.get_gene_annotations_by_gene_id('6934')
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

df = DatabaseClass.get_gene_annotations_by_gene_symbol('Gaijn@#_+')
print(df)
assert len(df)==0,                          "\033[91m Error11 : get_gene_annotations_by_gene_id \033[0m"
assert len(df.columns)==8,                  "\033[91m Error12 : get_gene_annotations_by_gene_id \033[0m"

#
# Test get_gene_annotations_by_gene_id
#
print('\n\033[94m TESTING: get_gene_annotations_by_snp \033[0m')
df = DatabaseClass.get_gene_annotations_by_snp('rs1801282')
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

df = DatabaseClass.get_gene_annotations_by_gene_symbol('Gaijn@#_+')
print(df)
assert len(df)==0,                          "\033[91m Error11 : get_gene_annotations_by_snp \033[0m"
assert len(df.columns)==8,                  "\033[91m Error12 : get_gene_annotations_by_snp \033[0m"

#
# Close Database Connection
#
DatabaseClass.db_close()
print ('\033[92m EVERYTHING IS WORKING \033[0m')