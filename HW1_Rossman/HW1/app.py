from flask import Flask, render_template
import joblib

app = Flask(__name__)

@app.route('/')
def index():

    # Return Template
    return render_template("index.html")
