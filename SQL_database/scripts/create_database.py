#create database in python shell
import sqlite3

#create & connect to the database 

db= sqlite3.connect('T2D_data.db')

db_cursor= db.cursor()
