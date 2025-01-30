import  sqlite3
import pandas as pd


#connect to the database
db= sqlite3.connect("T2D_data.db")

db_cursor = db.cursor()


# get the dataset csv file 
dataset= pd.read_csv('t2d.hugeamp_dataset/South_Asian/DIAMANTE_2022_T2D_GWAS_associations.csv')


#load the dataset into the database 
for i, row in dataset.iterrows():
    db_cursor.execute(''' INSERT INTO snp_information(dbSNP, chromosome, position, varID, nearest, pValue, zScore, alt, reference, ancestry)
    VALUES (?,?,?,?,?,?,?,?,?,?)''', (row['dbSNP'], row['chromosome'], row['position'], row['varID'],row['nearest'], row['pValue'], row['zScore'], row['alt'],row['reference'], row['ancestry']))

db.commit()

db_cursor.close()

db.close() 
