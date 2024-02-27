from datetime import datetime
from app import db

''' If this will work I'll kill myself
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
'''

attendance = db.Table("attendance",
    db.Column('user_id', db.Integer, db.ForeignKey('users.uid'), primary_key=True),
    db.Column('masterclass_id', db.Integer, db.ForeignKey('masterclasses.uid'), primary_key=True)
)

class User(db.Model):
    __tablename__='users'
    uid = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, unique=False)
    father_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    school_name = db.Column(db.String(128), index=True, unique=False)
    score=db.Column(db.Integer, default=0)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.login)

class MasterClass(db.Model):
    __tablename__="masterclasses"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=False)
    context = db.Column(db.Text)
    score = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship('User', secondary=attendance, lazy='dynamic', backref=db.backref('masterclasses', lazy=True))

    def __repr__(self):
        return '<Masteclass {}>'.format(self.name)
