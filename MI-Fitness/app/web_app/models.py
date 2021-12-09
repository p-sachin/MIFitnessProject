
from sqlalchemy.orm import backref
from web_app import db , login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    fname = db.Column(db.String(30),nullable=True)
    lname = db.Column(db.String(30),nullable=True)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(60),nullable=False)
    info = db.relationship('Fit_bio',backref='user',uselist=False)

    def __repr__(self):
        return f"User('{self.username},{self.email}')"

class Fit_bio(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    height = db.Column(db.Float,nullable=False)
    weight = db.Column(db.Float,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    gender = db.Column(db.String(4),nullable=False)
    bmi = db.Column(db.Float,nullable=False)
    dataset = db.Column(db.String(30),nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))



