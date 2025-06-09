from app import db
from flask_login import UserMixin
from datetime import datetime
from database.config import mysql_path

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column('ID_NO', db.Integer, primary_key=True, unique=True, autoincrement=True)
    email = db.Column('EMAIL_ADDRESS', db.String(50), unique=True, nullable=False)
    password = db.Column('PASS_WORD', db.String(60), nullable=False)
    account_type = db.Column('ACCOUNT_TYPE', db.String(25), nullable=False)
    first_name = db.Column('FIRST_NAME', db.String(50), nullable=False)
    middle_name = db.Column('MIDDLE_NAME', db.String(25), nullable=False)
    last_name = db.Column('LAST_NAME', db.String(50), nullable=False)
    prefix = db.Column('PREFIX', db.String(30), nullable=True)
    suffix = db.Column('SUFFIX', db.String(30), nullable=True)
    user_gender = db.Column('SEX', db.String(6), nullable=False)
    user_civil_status = db.Column('CIVIL_STATUS', db.String(20), nullable=False)
    user_citizenship = db.Column('COUNTRY_OF_CITIZENSHIP', db.String(70), nullable=False)
    date_of_birth = db.Column('DATE_OF_BIRTH', db.Date, nullable=False)
    country_birth = db.Column('COUNTRY_OF_BIRTH', db.String(70), nullable=False)
    contact_number = db.Column('CONTACT_NO', db.String(30), nullable=False)

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

    entry_no = db.Column('ENTRY_NO', db.Integer, primary_key=True)

    applicant_name = db.Column('FULL_NAME', db.String(50), nullable=False)
    alternative_name = db.Column('ALT_NAME', db.String(50), nullable=True)
    applicant_supporting_docs = db.Column('SUPPORTING_DOCS_NAME', db.String(100), nullable=False)
    applicant_DB = db.Column('BIRTH_DATE', db.Date, nullable=False)
    applicant_PB = db.Column('BIRTH_PLACE', db.String(50), nullable=False)
    applicant_gender = db.Column('GENDER', db.String(5), nullable=False)
    applicant_cs = db.Column('CIVIL_STATUS', db.String(10), nullable=False)
    ph_add = db.Column('PHILIPPINE_ADDRESS', db.String(100), nullable=False)
    ph_residence = db.Column('RESIDENCE_ADDRESS', db.String(100), nullable=False)
    applicant_mobile_no = db.Column('HOME_TELEPHONE_NO', db.String(20), nullable=False)
    work_tl_no = db.Column('WORK_TELEPHONE_NO', db.String(15), nullable=True)
    applicant_email = db.Column('EMAIL_ADDRESS', db.String(100), nullable=False)
    applicant_occupation = db.Column('PRESENT_OCCUPATION', db.String(50), nullable=False)
    work_address = db.Column('WORK_ADDRESS', db.String(100), nullable=False)

    
    ph_citizenship_id = db.Column('PH_CITIZENSHIP_ID', db.String(10), db.ForeignKey('philippine_citizenship.ph_citizenship_id'))
    id_no = db.Column('ID_NO', db.String(10), db.ForeignKey('user.id'), nullable=False)

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

    entry_no = db.Column('ENTRY_NO',db.Integer, db.ForeignKey('applicant.entry_no'))
    family_id = db.Column('FAMILY_ID', db.String(10), primary_key=True)  # made string for PK
    spouse_id = db.Column('SPOUSE_ID', db.String(10), db.ForeignKey('spouse_details.spouse_id'), nullable=False)

    family_name = db.Column('FAMILY_NAME', db.String(50), nullable=False)
    relation = db.Column('RELATION', db.String(50), nullable=False)
    citizenship = db.Column('FAMILY_CITIZENSHIP', db.String(50), nullable=False)
    
    spouse_details = db.relationship(
    'SpouseDetails',
    backref=db.backref('family_member', uselist=False),
    uselist=False,
    cascade="all, delete-orphan",
    single_parent=True
)

class SpouseDetails(db.Model):
    __tablename__ = 'spouse_details'

    spouse_id = db.Column('SPOUSE_ID', db.String(10), primary_key=True)
    spouse_address = db.Column('SPOUSE_ADDRESS', db.String(100), nullable=False)

class Overseas(db.Model):

    __tablename__ = 'overseas_citizenship'
    overseas_id = db.Column(db.String(10), primary_key=True)
    entry_no = db.Column('ENTRY_NO', db.Integer, db.ForeignKey('applicant.entry_no'), nullable=False)

    applicant_foreign_citizenship = db.Column('FOREIGN_CITIZENSHIP_ID', db.String(50), nullable=False)
    mode_of_acquisition = db.Column('ACQUISITION_FOREIGN_CITIZENSHIP', db.String(100), nullable=False)
    date_of_acquisition = db.Column('DATE_ACQUISITION', db.Date, nullable=False)
    natural_cert_numbers = db.Column('NATURALIZATION_NO', db.String(100), nullable=False)
    foreign_passport_no = db.Column('FOREIGN_PASSPORT_NO',db.String(50), nullable=False)
    date_of_issuance = db.Column('DATE_ISSUANCE', db.Date, nullable=False)
    place_of_issuance = db.Column('PLACE_ISSUANCE', db.String(100), nullable=False)
    foreign_docs= db.Column('FOREIGN_SUPPORTING_DOCS', db.String(50), nullable=False)

class Philippines(db.Model):
    __tablename__ = 'philippine_citizenship'

    ph_citizenship_id = db.Column('PH_CITIZENSHIP_ID',db.String(10), primary_key=True)
    ph_mode_of_aquisition = db.Column('MODE_PH_ACQUISITION', db.String(50), nullable=False)
    ph_docs = db.Column('PH_DOCS', db.String(50), nullable=False)

class Child(db.Model):
    __tablename__ = 'child'
    child_id = db.Column('CHILD_ID', db.String(10), primary_key=True)
    entry_no = db.Column('ENTRY_NO', db.Integer, db.ForeignKey('applicant.entry_no'), nullable=False)

    child_name = db.Column('CHILD_NAME', db.String(50), nullable=False)
    gender = db.Column('CHILD_GENDER', db.String(10), nullable=False)
    civil_status = db.Column('CHILD_CIVIL_STATUS',db.String(20), nullable=False)
    child_DB = db.Column('CHILD_DB', db.Date, nullable=False)
    child_PB = db.Column('CHILD_BP',db.String(75), nullable=False)
    country_pa = db.Column('COUNTRY_PA', db.String(75), nullable=False)
    child_citizenship = db.Column('CHILD_CITIZENSHIP', db.String(50), nullable=False)
    child_supporting_docs = db.Column('SUPPORTING_DOCS', db.String(100), nullable=False)
    immigration_docs = db.Column('IMMIGRATION_DOCS', db.String(100), nullable=False)
