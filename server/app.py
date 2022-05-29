from flask import Flask,request
import sqlite3

app = Flask(__name__)

#sqlite connector
def get_db_connection():
    conn = sqlite3.connect('quotes_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# get a number of quotes specified bu the request arg "number"
# example: http://127.0.0.1:5000/?number=3 returns three random quotes

@app.route("/random_quote", methods=['GET'])
def random_quote():
    conn = get_db_connection()
    number = request.args.get('number')

    res = {}

    if not (number.isdigit() and (int(number)>0 and int(number) <= 10)):
        res['error'] = 'number parameter must be an integer between 1 and 10'
        return res, 400

    query = 'SELECT * FROM quotes ORDER BY RANDOM() LIMIT ' + number
    cursor = conn.execute(query).fetchall()
    conn.close()

    quotes = []

    for quote in cursor:
        quotes.append({ 'quote' :quote['text'],'author':quote['name_author'],'info':quote['info_author']})

    res = { 'quotes' : quotes }

    return res, 200