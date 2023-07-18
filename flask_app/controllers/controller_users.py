from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.model_recipe import Recipe
bcrypt = Bcrypt(app)

from flask_app.models.model_user import User

@app.route('/')
def landing():
    return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        print(session['user_id'])
        return redirect ('/')
    recipes = Recipe.get_all()
    user = User.get_one(session['user_id'])
    # print("All is good!", recipes)
    return render_template('dashboard.html', recipes = recipes, user = user)


@app.route('/user/create', methods=["POST"])
def user_create():
    if not User.validate_user(request.form):
        return redirect('/')
    #GENERATES THE PASSWORD HASH
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    #RETYPE EVERYTHING DUE TO NEEDING TO INCORPORATE pw_hash VALUE
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    # save user into session
    user_id = User.write_user(data)
    session ['user_id'] = user_id
    print(user_id)
    return redirect('/dashboard/')

@app.route('/user/login', methods =["POST"])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.login(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard/")

    

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')


