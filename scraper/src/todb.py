path  = "../results/topics"
from ast import keyword
from os import listdir
files =  [path+'/'+author for author in listdir(path)]

import json

import sqlite3
con = sqlite3.connect('../../server/quotes_app.db')
cur = con.cursor()



counter = 0
for file in files:
    if not 'DS_Store' in file:
    #loop over files, each one contains all possible from an author
        with open(file) as f:
            data = json.load(f)

            for quote in data['quotes']:

                author = quote['author']
                topic = quote['keyword']
                text = quote['text']
       
                row = (author,topic,text)
                cur.execute("INSERT INTO quotes_topics VALUES (?,?,?)",row)
    


con.commit()
con.close()