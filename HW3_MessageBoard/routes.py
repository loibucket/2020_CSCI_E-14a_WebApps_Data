from dotenv import load_dotenv
from os import environ
from flask import Flask, redirect, render_template, jsonify, url_for

# Load environment
load_dotenv('.env')

# Initialize app
app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')

#import Heroku

app = Flask(__name__)
app.secret_key = "cscie14a-hw3"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hw3_db'

db.init_app(app)

#routes

if __name__ == "__main__":
    app.run(debug=True)




