from flask import Flask
import numpy
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!' 