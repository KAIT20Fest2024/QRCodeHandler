# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm
from app.models import User, MasterClass, attendance

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

@app.route("/scoreboard")
def scoreboard():
    mc = MasterClass.query.all()
    u = User.query.all()

    f = mc[0].users.filter(User.uid==1)
    print(f[0])
    return render_template("scoreboard.html", mc=mc)

@app.route("/qrhandler/<mcid>")
def qrhandler(mcid):
    mc = MasterClass.query.get(mcid)
    u = User.query.get(1)
    print(mc)
    if not(u in mc.users):
        u.score = u.score + mc.score
        mc.users.append(u)
        db.session.commit()
    else:
        print("error lol")
    
    return render_template("qrhandler.html", score=mc.score, user_score=u.score)

