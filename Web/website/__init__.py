from flask import Flask

app = Flask(__name__)

from app import app

app.run(debug=True)