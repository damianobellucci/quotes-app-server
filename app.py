from email.mime import application
from flask import Flask

application = Flask(__name__)


@application.route("/")
def ping():
    return 'ok'

