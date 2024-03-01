# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import qrcode, base64
from hashlib import shake_128

from app import app, db, login_manager
from app.forms import LoginForm, SignupForm
from app.models import User, MasterClass


# --- General ---
def make_mc_filename(mc_id: int):
    filename = f'masterclass{mc_id}'
    return shake_128(bytes(filename, 'utf-8')).hexdigest(len(filename))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<username>")
def profile(username: str):
    user = User.query.filter(User.login == username).first()
    unattended = [mc for mc in MasterClass.query.all() if not current_user in mc.users] if hasattr(current_user, 'login') and current_user.login == username else None
    return render_template("profile.html", user=user, unattended_mcs=unattended) if hasattr(user, 'uid') else redirect(url_for('index'))

@app.route("/scoreboard")
def scoreboard():
    users = User.query.order_by(User.score.desc()).filter(User.login != "ADMIN")
    return render_template("scoreboard.html", users=users)

@app.route("/qrhandler/<mc_hash>")
@login_required
def qrhandler(mc_hash):
    mc = MasterClass.query.filter(MasterClass.hash == mc_hash).first()

    if not mc or current_user in mc.users: return redirect(url_for("profile", username=current_user.login))

    current_user.score += mc.score
    mc.users.append(current_user)
    db.session.commit()
    return render_template("qrhandler.html", mc_score=mc.score, user_score=current_user.score)


# --- Account management --- 
@login_manager.user_loader
def user_loader(uid: int):
    return User.query.get(int(uid))

@login_manager.unauthorized_handler
def unathorized():
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(login=form.username.data, 
                        first_name=form.fname.data, 
                        father_name=form.mname.data, 
                        last_name=form.lname.data, 
                        school_name=form.school.data, 
                        password=form.password.data,
                        )
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
        else: flash("Wrong credentials")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
def logout():
    username = current_user.login
    logout_user()
    return redirect(url_for("profile", username=username))


# --- Admin stuff ---
def admin_required(route):
    def admin_wrapper(*args, **kwargs):
        if current_user.login == "ADMIN": return route(*args, **kwargs)
        return redirect(url_for("index"))
    return admin_wrapper

@admin_required
@app.route("/admin", methods=["GET"])
def admin():
    mcs = MasterClass.query.all()
    return render_template("admin.html", mc=mcs)

@admin_required
@app.route("/admin/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        mc = MasterClass(name=request.form.get('name'), context=request.form.get('context'), score=request.form.get('score'))
        db.session.add(mc)
        db.session.commit()
        filename = make_mc_filename(mc.uid)
        mc.hash = filename
        print(f'FILENAME FOR {mc.uid}: {filename}')
        db.session.commit()

        img = qrcode.make(f"localhost/qrhandler/{filename}")
        img.save(f"app/{url_for('static', filename='qr/')}{filename}.png")

        return redirect(url_for('admin'))

    return render_template("create.html")

@admin_required
@app.route("/admin/edit/<mc_id>", methods=["GET", "POST"])
def edit(mc_id):
    mc = MasterClass.query.get(mc_id)
    if mc:
        if request.method == 'GET': return render_template("edit.html", mc=mc)
        mc.name = request.form.get('mc_name')
        mc.context = request.form.get('context')
        mc.score = request.form.get('score')
        db.session.commit()
    return redirect(url_for('admin'))

