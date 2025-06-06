from app import db
from flask_login import UserMixin
from datetime import datetime
from database.config import mysql_path

class User(db.Model, UserMixin):
    id_no = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_type = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    prefix = db.Column(db.String(5), nullable=True)
    suffix = db.Column(db.String(7), nullable=True)
    user_gender = db.Column(db.String(2), nullable=False)
    user_civil_status = db.Column(db.String(2), nullable=False)
    user_citizenship = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    country_birth = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(18), nullable=False)
    
    applicants = db.relationship('Applicant', backref='user', lazy=True)

class UserFunction(db.Model):
    __tablename__ = 'user_function'

    entry_no = db.Column(
        db.Integer,
        db.ForeignKey('applicant.entry_no'),
        primary_key=True 
    )
    location = db.Column(db.String(50), nullable=False)
    transaction = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    applicant = db.relationship('Applicant', backref=db.backref('user_function', uselist=False))

class Applicant(db.Model):
    __tablename__ = 'applicant'

    entry_no = db.Column(db.Integer, primary_key=True)

    applicant_name = db.Column(db.String(50), nullable=False)
    alternative_name = db.Column(db.String(50), nullable=True)
    applicant_supporting_docs = db.Column(db.String(100), nullable=False)
    applicant_DB = db.Column(db.Date, nullable=False)
    applicant_PB = db.Column(db.String(50), nullable=False)
    applicant_gender = db.Column(db.String(5), nullable=False)
    applicant_cs = db.Column(db.String(10), nullable=False)
    ph_add = db.Column(db.String(100), nullable=False)
    ph_residence = db.Column(db.String(100), nullable=False)
    applicant_mobile_no = db.Column(db.String(20), nullable=False)
    work_tl_no = db.Column(db.String(15), nullable=True)
    applicant_email = db.Column(db.String(100), nullable=False)
    applicant_occupation = db.Column(db.String(50), nullable=False)
    work_address = db.Column(db.String(100), nullable=False)

    
    ph_citizenship_id = db.Column(db.String(10), db.ForeignKey('philippine_citizenship.ph_citizenship_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_no'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    family_members = db.relationship(
        'FamilyMember',
        backref='applicant',
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys='FamilyMember.entry_no'
    )
    overseas_entries = db.relationship(
        'Overseas',
        backref='applicant',
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys='Overseas.entry_no'
    )

    children = db.relationship(
        'Child', 
        backref='applicant', 
        lazy=True, 
        cascade="all, delete-orphan",
        foreign_keys='Child.entry_no')

class FamilyMember(db.Model):
    
    __tablename__ = 'family_member'

    entry_no = db.Column(db.Integer, db.ForeignKey('applicant.entry_no'))
    family_id = db.Column(db.String(10), primary_key=True)  # made string for PK
    spouse_id = db.Column(db.String(10), db.ForeignKey('spouse_details.spouse_id'), nullable=False)

    family_name = db.Column(db.String(50), nullable=False)
    relation = db.Column(db.String(50), nullable=False)
    citizenship = db.Column(db.String(50), nullable=False)
    
    spouse_details = db.relationship('SpouseDetails', backref='family_member', uselist=False, cascade="all, delete-orphan")

class SpouseDetails(db.Model):
    __tablename__ = 'spouse_details'

    spouse_id = db.Column(db.String(10), primary_key=True)
    spouse_address = db.Column(db.String(100), nullable=False)

class Overseas(db.Model):

    __tablename__ = 'overseas_citizenship'
    overseas_id = db.Column(db.String(10), primary_key=True)
    entry_no = db.Column(db.Integer, db.ForeignKey('applicant.entry_no'), nullable=False)

    applicant_foreign_citizenship = db.Column(db.String(50), nullable=False)
    mode_of_acquisition = db.Column(db.String(100), nullable=False)
    date_of_acquisition = db.Column(db.Date, nullable=False)
    natural_cert_numbers = db.Column(db.String(100), nullable=False)
    foreign_passport_no = db.Column(db.String(50), nullable=False)
    date_of_issuance = db.Column(db.Date, nullable=False)
    place_of_issuance = db.Column(db.String(100), nullable=False)
    foreign_docs= db.Column(db.String(50), nullable=False)

class Philippines(db.Model):
    __tablename__ = 'philippine_citizenship'

    ph_citizenship_id = db.Column(db.String(10), primary_key=True)
    ph_mode_of_aquisition = db.Column(db.String(50), nullable=False)
    ph_docs = db.Column(db.String(50), nullable=False)

class Child(db.Model):
    __tablename__ = 'child'
    child_id = db.Column(db.String(10), primary_key=True)
    entry_no = db.Column(db.Integer, db.ForeignKey('applicant.entry_no'), nullable=False)

    child_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    civil_status = db.Column(db.String(20), nullable=False)
    child_DB = db.Column(db.Date, nullable=False)
    child_PB = db.Column(db.String(75), nullable=False)
    country_pa = db.Column(db.String(75), nullable=False)
    child_citizenship = db.Column(db.String(50), nullable=False)
    child_supporting_docs = db.Column(db.String(100), nullable=False)
    immigration_docs = db.Column(db.String(100), nullable=False)
