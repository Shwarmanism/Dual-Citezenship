from app import db
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    id_no = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_type = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    prefix = db.Column(db.String(5), nullable=True)
    suffix = db.Column(db.String(7), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.column(db.String(18), nullable=False)
    petitions = db.relationship('Petition', backref='user', lazy=True)

class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    
    spouse_first_name = db.Column(db.String(50))
    spouse_middle_name = db.Column(db.String(50))
    spouse_last_name = db.Column(db.String(50))
    spouse_citizenship = db.Column(db.String(50))

    #other fields located the form_routes.py

    children = db.relationship('PetitionChild', backref='petition', lazy=True, cascade="all, delete-orphan")


class PetitionChild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petition.id'), nullable=False)
    
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    civil_status = db.Column(db.String(20))
    dob = db.Column(db.Date)
    pob = db.Column(db.String(100))
    citizenship = db.Column(db.String(50))
    perm_address = db.Column(db.String(100))
    supporting_docs = db.Column(db.String(200))

