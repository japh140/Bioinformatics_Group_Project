

import sqlite3

import pandas as pd

# load population metadata csv file

df = pd.read_csv("t2d.hugeamp_dataset/population_metadata_from_1000_Genome.csv", sep="\t")  


# df with relevant columns only
df = df[['Sample name', 'Population name']]


#connect to the database
db= sqlite3.connect("T2D_data.db")

db_cursor = db.cursor()




# create table for Population info
db_cursor.execute(''' CREATE TABLE population_information (sample_ID TEXT PRIMARY KEY, population TEXT)''')

# Insert data into the table
df.to_sql("population_information", db, if_exists="replace", index=False)


# update and close the database connection 
db.commit ()

db_cursor.close()

db.close() 

print ('population information table created and loaded in the databse')
