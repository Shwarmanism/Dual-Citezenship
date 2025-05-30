from app import db
from flask_login import UserMixin
from datetime import datetime

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
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(18), nullable=False)

    applicants = db.relationship('Applicant', backref='user', lazy=True)

class Applicant(db.Model):
    entry_no = db.Column(db.Integer, primary_key=True)

    applcant_name = db.Column(db.String(50), nullable=False)
    alternative_name = db.Column(db.String(50), nullable=True)
    applicant_supporting_docs = db.Column(db.String(100), nullable=False)
    applicant_DB = db.Column(db.Date, nullable=False)
    applicant_PB = db.Column(db.String(50), nullable=False)
    applicant_gender = db.Column(db.String(5), nullable=False)
    applicant_cs = db.Column(db.String(10), nullable=False)
    ph_add = db.Column(db.String(100), nullable=False)
    ph_residence = db.Column(db.String(100), nullable=False)
    applicant_mobile_no = db.Column(db.String(20), nullable=False)
    applicant_email = db.Column(db.String(100), nullable=False)
    applicant_occupation = db.Column(db.String(50), nullable=False)
    work_address = db.Column(db.String(100), nullable=False)
    
    spouse_id = db.Column(db.String(10), db.ForeignKey('SpouseDetails.spouse_id'), nullable=False)
    family_id = db.Column(db.String(10), db.ForeignKey('FamilyMembers.family_id'), nullable=False)
    overseas_id = db.Column(db.String(10), db.ForeignKey('Overseas.overseas_id', nullable=False))
    ph_id = db.Column(db.String(10), db.ForeignKey('Philippines.ph_id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id_no'), nullable=False)  # link Applicant to User
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    family_members = db.relationship('FamilyMember', backref='Applicant', lazy=True, cascade="all, delete-orphan")
    overseas_entries = db.relationship('Overseas', backref='Applicant', lazy=True, cascade="all, delete-orphan")
    children = db.relationship('Child', backref='Applicant', lazy=True, cascade="all, delete-orphan")

class FamilyMember(db.Model):
    family_id = db.Column(db.Integer, primary_key=True)  # made int for easier PK
    entry_no = db.Column(db.Integer, db.ForeignKey('Applicant.entry_no'), nullable=False)

    family_name = db.Column(db.String(50), nullable=False)
    relation = db.Column(db.String(50), nullable=False)
    citizenship = db.Column(db.String(50), nullable=False)

    spouse_details = db.relationship('SpouseDetails', backref='FamilyMember', uselist=False, cascade="all, delete-orphan")

class SpouseDetails(db.Model):
    family_id = db.Column(db.Integer, db.ForeignKey('FamilyMember.family_id'), nullable=False)
    spouse_address = db.Column(db.String(100), nullable=False)

class Overseas(db.Model):
    overseas_id = db.Column(db.Integer, primary_key=True)
    entry_no = db.Column(db.Integer, db.ForeignKey('Applicant.entry_no'), nullable=False)

    foreign_add = db.Column(db.String(100), nullable=False)
    applicant_foreign_citizenship = db.Column(db.String(50), nullable=False)
    mode_of_acquisition = db.Column(db.String(100), nullable=False)
    date_of_acquisition = db.Column(db.Date, nullable=False)
    natural_cert_numbers = db.Column(db.String(100), nullable=False)
    foreign_passport_no = db.Column(db.String(50), nullable=False)
    issuance_of_foreign_passport = db.Column(db.String(100), nullable=False)
    place_of_issuance = db.Column(db.String(100), nullable=False)
    foreign_docs= db.Column(db.String(50), nullable=False)

class Philippines(db.Model):
    ph_id = db.Column(db.Integer, primary_key=True)
    ph_mode_of_aquisition = db.Column(db.String(50), nullable=False)
    ph_docs = db.Column(db.String(50), nullable=False)

class Child(db.Model):
    child_id = db.Column(db.Integer, primary_key=True)
    entry_no = db.Column(db.Integer, db.ForeignKey('Applicant.entry_no'), nullable=False)

    child_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    civil_status = db.Column(db.String(20), nullable=False)
    child_DB = db.Column(db.Date, nullable=False)
    child_PB = db.Column(db.String(75), nullable=False)
    country_pa = db.Column(db.String(75), nullable=False)
    child_citizenship = db.Column(db.String(50), nullable=False)
    child_supporting_docs = db.Column(db.String(100), nullable=False)
    immigration_docs = db.Column(db.String(100), nullable=False)
