# -*- coding: utf-8 -*-
from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    userModel = {'username': 'admin'}
    return render_template("index.html", user=userModel)
