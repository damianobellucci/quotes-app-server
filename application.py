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

@app.route("/ping", methods=['GET'])
def ping():
    return 'ok',200


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #app.debug = True
    app.run()