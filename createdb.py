import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE files (user TEXT, filename TEXT, file BLOB)')
print ("Table created successfully")
conn.close()
