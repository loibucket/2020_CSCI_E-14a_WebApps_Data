from flask import Flask, flash, render_template, request, url_for, redirect, jsonify, session
from flask_migrate import Migrate

from models.models import Db, User, Post, Follow
from forms.forms import SignupForm, LoginForm, NewpostForm
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from os import environ

import sys

load_dotenv('.env')

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')

# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost/hw3_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Db.init_app(app)
migrate = Migrate(app, Db)


def make_post(name, content, dtime):
    return name + " : " + content + " | " + dtime.strftime("%m/%d/%Y, %H:%M:%S")


# GET /
@app.route('/')
@app.route('/index')
def index():
    # map uid and usernames
    u = {}
    all_users = User.query.all()
    for user in all_users:
        u[user.uid] = user.username

    if 'username' in session:
        m = "Welcome " + session['username'] + "! You and Your Followers"
        # user object
        session_user = User.query.filter_by(username=session['username']).first()
        # user and followers id list
        fids = [session_user.uid] + [f.following for f in Follow.query.filter_by(follower=session_user.uid)]
        # filter posts
        posts = Post.query.filter(Post.uid.in_(fids)).all()
        posts_out = [make_post(u[p.uid], p.content, p.datetime) for p in posts]
        return render_template('index.html', message=m, title='Home', posts=posts_out,
                               session_username=session_user.username)

    else:
        m = "All posts are listed here. To create a followers group, please log-in or sign - up."
        posts_out = [make_post(u[p.uid], p.content, p.datetime) for p in Post.query.all()]
        return render_template('index.html', message=m, title='Home', posts=posts_out)


# GET & POST /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Init form
    form = LoginForm()

    # If post
    if request.method == 'POST':

        # Init credentials from form request
        username = request.form['username']
        password = request.form['password']

        # Init user by Db query
        user = User.query.filter_by(username=username).first()

        # Control login validity
        if user is None or not sha256_crypt.verify(password, user.password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            session['username'] = username
            return redirect(url_for('index'))

    # If GET
    else:
        return render_template('login.html', title='Login', form=form)


# GET & POST /newpost
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    # Init form
    form = NewpostForm()

    # If POST
    if request.method == 'POST':

        # Init user from poster
        session_user = User.query.filter_by(
            username=session['username']).first()

        # Init content from form request
        content = request.form['content']

        # Create in DB
        new_post = Post(uid=session_user.uid, content=content)
        Db.session.add(new_post)
        Db.session.commit()

        return redirect(url_for('index'))

    # If GET
    else:
        return render_template('newpost.html', title='Newpost', form=form)


# GET & POST /signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Init form
    form = SignupForm()

    # IF POST
    if request.method == 'POST':

        # Init credentials from form request
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        # Init user from Db query
        existing_user = User.query.filter_by(username=username).first()

        if password_repeat != password:
            flash('The username and password does not match!')
            return redirect(url_for('signup'))

        # Control new credentials
        if existing_user:
            flash('The username already exists. Please pick another one.')
            return redirect(url_for('signup'))
        else:
            user = User(username=username,
                        password=sha256_crypt.hash(password))
            Db.session.add(user)
            Db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))

    # IF GET
    else:
        return render_template('signup.html', title='Signup', form=form)


# POST /logout
@app.route('/logout', methods=['POST'])
def logout():
    # Logout
    session.clear()
    return redirect(url_for('index'))


# no profile
@app.route('/profile', methods=['GET'])
@app.route('/profile/', methods=['GET'])
def no_profile():
    flash('Profile not found!')
    return redirect(url_for('index'))


# GET /profile/<username>
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    # Control by login status
    if 'username' in session:

        # Retrieve session user
        session_user = User.query.filter_by(
            username=session['username']).first()

        # Retrieve profile user
        profile_user = User.query.filter_by(username=username).first()

        # user not found
        if profile_user is None:
            flash('Profile not found!')
            return redirect(url_for('index'))

        # session and profile user are same
        same_person = False
        if profile_user == session_user:
            same_person = True

        # Retrieve posts
        profile_user_posts = Post.query.filter_by(uid=profile_user.uid).all()
        posts_out = [make_post(username, p.content, p.datetime) for p in profile_user_posts]

        # Check to see if follow relationship exists
        followed = False
        if Follow.query.filter_by(follower=session_user.uid, following=profile_user.uid).count() > 0:
            followed = True

        return render_template('profile.html', user=profile_user, message="", title='Profile', posts=posts_out,
                               followed=followed, same_person=same_person)
    else:
        flash('You must be logged in to search!')
        return redirect(url_for('index'))


# GET /profile/<username>/follow
@app.route('/profile/<username>/follow', methods=['POST'])
def follow(username):
    # Retrieve session user
    session_user = User.query.filter_by(username=session['username']).first()

    # Retrieve profile user
    profile_user = User.query.filter_by(username=username).first()

    # Add Follow entry
    follow = Follow(follower=session_user.uid, following=profile_user.uid)
    Db.session.add(follow)
    Db.session.commit()

    return redirect(url_for('profile', username=username))


# GET /profile/<username>/unfollow
@app.route('/profile/<username>/unfollow', methods=['POST'])
def unfollow(username):
    # Retrieve session user
    session_user = User.query.filter_by(username=session['username']).first()

    # Retrieve profile user
    profile_user = User.query.filter_by(username=username).first()

    # Remove entry
    follow = Follow.query.filter_by(
        follower=session_user.uid, following=profile_user.uid).first()
    Db.session.delete(follow)
    Db.session.commit()

    return redirect(url_for('profile', username=username))
