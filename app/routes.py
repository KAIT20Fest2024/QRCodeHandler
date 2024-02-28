# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from app import app, db, login_manager
from app.forms import LoginForm, SignupForm

from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from app.models import User, MasterClass

import qrcode, base64


def admin_required(route):
    def admin_wrapper(*args, **kwargs):
        if current_user.login == "ADMIN":
            return route(*args, **kwargs)
        else:
            return redirect(url_for("index"))
    return admin_wrapper


@login_manager.user_loader
def user_loader(uid: int):
    return User.query.get(int(uid))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

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

@login_manager.unauthorized_handler
def unathorized():
    return redirect(url_for("login"))

@app.route("/user/<username>")
def profile(username: str):
    user = User.query.filter(User.login == username).first()
    return render_template("profile.html", user=user) if hasattr(user, 'uid') else redirect(url_for('index'))

@admin_required
@app.route("/admin", methods=["GET", "POST"])
def admin():
    masterClasses = MasterClass.query.all()
    for m in masterClasses:
        img = qrcode.make(f"localhost/qrhandler/{m.uid}")
        img.save('app/'+url_for('static', filename='qr/')+str(m.uid)+'.png')
    return render_template("admin.html", mc = masterClasses)

@admin_required
@app.route("/admin/edit/<count>", methods=["GET", "POST"])
def edit(count):
    mc = MasterClass.query.get(count)
    if mc:
        if request.method == 'GET':
            return render_template("edit.html", mc=mc)
        mc.name = request.form.get('mc_name')
        mc.context = request.form.get('context')
        mc.score = request.form.get('score')
        db.session.commit()
    return redirect(url_for('admin'))

@admin_required
@app.route("/admin/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        mc = MasterClass(name=request.form.get('name'),context=request.form.get('context'),score=request.form.get('score'))
        db.session.add(mc)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template("create.html")

@app.route("/scoreboard")
def scoreboard():
    users = User.query.order_by(User.score.desc())
    return render_template("scoreboard.html", users=users)

@app.route("/qrhandler/<mcid>")
@login_required
def qrhandler(mcid):
    mc = MasterClass.query.get(mcid)

    if current_user in mc.users:
        return redirect(url_for("profile", username=current_user.login))
    else:
        current_user.score += mc.score
        mc.users.append(current_user)
        db.session.commit()
    
    return render_template("qrhandler.html", mc_score=mc.score, user_score=current_user.score)

