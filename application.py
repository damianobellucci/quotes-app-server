from flask import Flask,request
from flask_cors import CORS
import sqlite3
from uuid import uuid4

app = Flask(__name__)
CORS(app)


@app.route("/ping", methods=['GET'])
def ping():
    return 'ok',200


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #app.debug = True
    app.run()