import  sqlite3

#connect to the database
db= sqlite3.connect("T2D_data.db")

db_cursor = db.cursor()


#create table for snp inofrmation

db_cursor.execute(''' CREATE TABLE  snp_information ( dbSNP TEXT PRIMARY KEY, chromosome INTEGER, position INTEGER, varID TEXT, nearest TEXT, pValue REAL, zScore REAL, alt TEXT, reference TEXT, ancestry TEXT)''')

#update and close the database connection 
db.commit ()

db_cursor.close()

db.close() 

