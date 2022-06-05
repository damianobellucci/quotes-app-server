from flask import Flask

app = Flask(__name__)

<<<<<<< HEAD
@app.route("/", methods=['GET'])
=======

@app.route("/ping", methods=['GET'])
>>>>>>> 56514b35444ab877a24e58c4c0e3d82fdc944c97
def ping():
    return 'ok'