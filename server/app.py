from flask import Flask,request
from flask_cors import CORS
import sqlite3
from uuid import uuid4

app = Flask(__name__)
CORS(app)

#sqlite connector
def get_db_connection():
    conn = sqlite3.connect('quotes_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# get a number of quotes specified bu the request arg "number"
# example: http://127.0.0.1:5000/random_quote?number=3 returns a JSON object with a list of three random quotes

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

@app.route("/login", methods=['POST'])
def login():
    
    conn = get_db_connection()

    username = request.json['username']
    password = request.json['password']

    query = 'SELECT * FROM accounts WHERE username=? AND password=?'

    cursor = conn.execute(query,(username,password)).fetchall()
    conn.close()

  
    for account in cursor:
        print(account['username'],account['password'])

    if len(cursor) == 0:
        return {'error':'login error'}, 400
    
    else:
        token = uuid4().hex
        try:
            conn = get_db_connection()
            query = 'insert into tokens values(?,?)'
            cursor = conn.execute(query,(token,username)).fetchall()
            conn.commit()
            conn.close()
        except Exception as exeption:
            print(exeption)
            return {'error':'register failure'}, 400
  
        return {'token':token}, 200


@app.route("/register", methods=['POST'])
def register():

    username = request.json['username']
    password = request.json['password']
    
    try:
        conn = get_db_connection()
        query = 'insert into accounts values(?,?)'
        cursor = conn.execute(query,(username,password)).fetchall()
        conn.commit()
    except:
        return {'error':'register failure'}, 400
    
    conn.close()
    return {'success':'register success'}, 200


@app.route("/info-account", methods=['GET'])
def info_account():

    token = request.json['token']
    
    try:
        conn = get_db_connection()
        query = 'SELECT * FROM tokens WHERE token=? LIMIT 1'
        result = conn.execute(query,(token,)).fetchall()
        for info in result:
            print(info['token'],info['username'])
        conn.close()
        #...other queries to retrieve other infos
        data = {'username':info['username']}
        return data, 200

    except:
        return {'error':'error in getting info account by token'}, 400
    