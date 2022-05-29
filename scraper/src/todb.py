path  = "../results/final-result"
from os import listdir
files =  [path+'/'+author for author in listdir(path)]

import json

import sqlite3
con = sqlite3.connect('quotes_app.db')
cur = con.cursor()

counter = 0
for file in files:
    #loop over files, each one contains all possible from an author
    with open(file) as f:
        author_id = counter
        counter += 1
        data = json.load(f)
        name_author = data['author']['name']
        info_author = data['author']['info_html']['info_string']
        url_author = data['author']['url']
        quotes_author = [quote['text'].replace("\n","") for quote in data['quotes']]

        for quote in quotes_author:
            row = (str(author_id),name_author,info_author,url_author,quote)
            cur.execute("INSERT INTO quotes VALUES (?,?,?,?,?)",row)



con.commit()
con.close()