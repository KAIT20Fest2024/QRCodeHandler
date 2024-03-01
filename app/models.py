from datetime import datetime
from app import db
from flask_login import UserMixin


attendance = db.Table("attendance",
    db.Column('user_id', db.Integer, db.ForeignKey('users.uid'), primary_key=True),
    db.Column('masterclass_id', db.Integer, db.ForeignKey('masterclasses.uid'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__='users'
    uid = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, unique=False)
    father_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    school_name = db.Column(db.String(128), index=True, unique=False)
    score=db.Column(db.Integer, default=0)
    password = db.Column(db.String(128))

    def get_id(self):
        return self.uid

    def __repr__(self):
        return '<User {}>'.format(self.login)

class MasterClass(db.Model):
    __tablename__="masterclasses"
    uid = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(128), index=True, unique=False)
    context = db.Column(db.Text)
    score = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship('User', secondary=attendance, lazy='dynamic', backref=db.backref('masterclasses', lazy=True))

    def __repr__(self):
        return '<Masteclass {}>'.format(self.name)
