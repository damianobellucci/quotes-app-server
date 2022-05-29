import sqlite3

from pkg_resources import ContextualVersionConflict
con = sqlite3.connect('quotes_app.db')
cur = con.cursor()

cursor = cur.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1')

print(cursor[0])