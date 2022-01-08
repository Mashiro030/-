import sqlite3
import io

DATABASE = './db.sqlite'

db = sqlite3.connect(DATABASE)
cursor = db.cursor()

with open('init.sql') as f:
    db.executescript(f.read())

# Show all the tables, equivalent to "SHOW tables" in MySQL
res = db.execute('''
    SELECT name FROM sqlite_master
    WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%'
''')

print(list(res))