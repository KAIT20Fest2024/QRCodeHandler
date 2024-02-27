# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash
from app import app, db, login_manager
from app.forms import LoginForm, SignupForm

from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from app.models import User


@login_manager.user_loader
def user_loader(uid: int):
    return User.query.get(int(uid))


@app.route("/")
@app.route("/index")
def index():
    userModel = {'username': 'admin'}
    return render_template("index.html", user=userModel)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(login=form.username.data, first_name=form.fname.data, father_name=form.mname.data, last_name=form.lname.data, school_name=form.school.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('profile', username=form.username.data))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile", username=current_user.login))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data, password=form.password.data).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("profile", username=user.login))
        else:
            flash("Wrong credentials")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
def logout():
    username = current_user.login
    logout_user()
    return redirect(url_for("profile", username=username))

@app.route("/user/<username>")
def profile(username: str):
    user = User.query.filter(User.login == username).first()
    return render_template("profile.html", user=user) if hasattr(user, 'uid') else redirect(url_for('index'))
