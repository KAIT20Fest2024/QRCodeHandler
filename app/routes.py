# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm
from app.models import User, MasterClass
import qrcode, base64

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

@app.route("/admin", methods=["GET", "POST"])
def admin():
    masterClasses = MasterClass.query.all()
    for m in masterClasses:
        img = qrcode.make(f"localhost/qrhandler/{m.uid}")
        img.save('app/'+url_for('static', filename='qr/')+str(m.uid)+'.png')
    return render_template("admin.html", mc = masterClasses)

@app.route("/admin/edit/<count>", methods=["GET", "POST"])
def edit(count):
    if request.method == "POST":
        mc = MasterClass.query.filter_by(uid=count).first()
        mc.name = request.form.get('name')
        mc.context = request.form.get('context')
        mc.score = request.form.get('score')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template("edit.html")

@app.route("/admin/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        mc = MasterClass(name=request.form.get('name'),context=request.form.get('context'),score=request.form.get('score'))
        db.session.add(mc)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template("create.html")