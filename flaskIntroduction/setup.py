import sqlite3

conn = sqlite3.connect("movieData.db")
conn.execute("CREATE TABLE Reviews (Username TEXT, MovieID TEXT, ReviewTime DATETIME, Rating FLOAT, Review TEXT)")
conn.execute("CREATE TABLE Movies (MovieID TEXT PRIMARY KEY, Title TEXT, Director TEXT, Genre TEXT, Year INTEGER(4))")
conn.close()