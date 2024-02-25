# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    userModel = {'username': 'admin'}
    return render_template("index.html", user=userModel)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template("login.html", form=form)
