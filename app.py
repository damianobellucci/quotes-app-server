from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET'])
def ping():
    return 'ok'

if __name__ == "__main__":
    app.run()