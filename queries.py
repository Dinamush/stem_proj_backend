import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())  # This will list all the tables in the database
