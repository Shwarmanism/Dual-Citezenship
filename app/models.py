from app import db
from flask_login import UserMixin
from datetime import datetime
from database.config import mysql_path

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id_no = db.Column('ID_NO', db.Integer, primary_key=True, unique=True, autoincrement=True)
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

    def get_id(self):
        return str(self.id_no)
    
class UserFunction(db.Model):
    __tablename__ = 'user_function'

    entry_no = db.Column(
        'FK_USERF_ENTRY_NO',
        db.Integer,
        db.ForeignKey('applicant.ENTRY_NO'),
        primary_key=True 
    )
    location = db.Column('LOCATION',db.String(50), nullable=False)
    transaction = db.Column('TRANSACTION', db.String(30), nullable=False)
    status = db.Column('STATUS',db.String(10), nullable=False)
    created_at = db.Column('CREATED_AT', db.DateTime, default=datetime.utcnow, nullable=False)
    date_updated = db.Column('DATE_UPDATED', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)    

    applicant = db.relationship(
    'Applicant',
    backref=db.backref('user_function', 
    uselist=False, 
    cascade="all, delete-orphan")
    )

class Applicant(db.Model):
    __tablename__ = 'applicant'

    entry_no = db.Column('ENTRY_NO', db.Integer, primary_key=True, autoincrement=True)

    applicant_name = db.Column('FULL_NAME', db.String(50), nullable=False)
    alternative_name = db.Column('ALT_NAME', db.String(50))
    applicant_supporting_docs = db.Column('SUPPORTING_DOCS_NAME', db.String(100))
    applicant_DB = db.Column('BIRTH_DATE', db.Date, nullable=False)
    applicant_PB = db.Column('BIRTH_PLACE', db.String(50), nullable=False)
    applicant_gender = db.Column('GENDER', db.String(5), nullable=False)
    applicant_cs = db.Column('CIVIL_STATUS', db.String(50), nullable=False)
    philippine_address = db.Column('PHILIPPINE_ADDRESS', db.String(100), nullable=False)
    ph_residence = db.Column('RESIDENCE_ADDRESS', db.String(100), nullable=False)
    home_telephone_no = db.Column('HOME_TELEPHONE_NO', db.String(20), nullable=True)
    work_tl_no = db.Column('WORK_TELEPHONE_NO', db.String(15), nullable=True)
    applicant_email = db.Column('EMAIL_ADDRESS', db.String(100), nullable=False)
    applicant_occupation = db.Column('PRESENT_OCCUPATION', db.String(50), nullable=False)
    work_address = db.Column('WORK_ADDRESS', db.String(100), nullable=False)

    ph_citizenship_id = db.Column('PH_CITIZENSHIP_ID', db.String(50), db.ForeignKey('philippine_citizenship.PH_CITIZENSHIP_ID'))
    id_no = db.Column('ID_NO', db.Integer, db.ForeignKey('user.ID_NO'), nullable=False)
    
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
        foreign_keys='Child.entry_no'
    )

    philippine = db.relationship(
    'Philippines',
    backref='applicant',
    uselist=False,
    foreign_keys='Applicant.ph_citizenship_id'
    )

class FamilyMember(db.Model):
    __tablename__ = 'family_member'

    entry_no = db.Column('ENTRY_NO', db.Integer, db.ForeignKey('applicant.ENTRY_NO'))
    family_id = db.Column('FAMILY_ID', db.String(10), primary_key=True, nullable=True)
    spouse_id = db.Column('SPOUSE_ID', db.String(10), db.ForeignKey('spouse_details.SPOUSE_ID'), nullable=True)

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

    foreign_id = db.Column('FOREIGN_CITIZENSHIP_ID', db.String(50), primary_key=True)  # match varchar(7)
    entry_no = db.Column('FK_OVERSEAS_ENTRY_NO', db.Integer, db.ForeignKey('applicant.ENTRY_NO'), nullable=False)

    applicant_foreign_citizenship = db.Column('FOREIGN_CITIZENSHIP', db.String(50), nullable=False)
    acquisition_foreign_citizenship = db.Column('ACQUISITION_FOREIGN_CITIZENSHIP', db.String(45), nullable=False)
    date_acquisition = db.Column('DATE_ACQUISITION', db.Date, nullable=False)
    naturalization_no = db.Column('NATURALIZATION_NO', db.String(15), nullable=False)
    foreign_passport_no = db.Column('FOREIGN_PASSPORT_NO', db.String(15), nullable=False)
    date_issuance = db.Column('DATE_ISSUANCE', db.Date, nullable=False)
    place_issuance = db.Column('PLACE_ISSUANCE', db.String(70), nullable=False)
    foreign_supporting_docs = db.Column('FOREIGN_ACQUISITION_DOCS', db.String(40), nullable=False)

class Philippines(db.Model):
    __tablename__ = 'philippine_citizenship'

    ph_citizenship_id = db.Column('PH_CITIZENSHIP_ID', db.String(50), primary_key=True)
    mode_ph_acquisition = db.Column('MODE_PH_ACQUISITION', db.String(50), nullable=False)
    ph_docs = db.Column('PH_DOCS', db.String(255), nullable=False)

class Child(db.Model):
    __tablename__ = 'child'

    child_id = db.Column('CHILD_ID', db.String(50), primary_key=True)
    entry_no = db.Column('FK_CHILD_ENTRY_NO', db.Integer, db.ForeignKey('applicant.ENTRY_NO'), nullable=False)

    child_name = db.Column('CHILD_NAME', db.String(50), nullable=False)
    child_gender = db.Column('CHILD_GENDER', db.String(10), nullable=False)
    child_civil_status = db.Column('CHILD_CIVIL_STATUS', db.String(20), nullable=False)
    child_BD = db.Column('CHILD_BD', db.Date, nullable=False)
    child_PB = db.Column('CHILD_BP', db.String(75), nullable=False)
    country_pa = db.Column('COUNTRY_PA', db.String(75), nullable=False)
    child_citizenship = db.Column('CHILD_CITIZENSHIP', db.String(50), nullable=False)
    child_supporting_docs = db.Column('SUPPORTING_DOCS', db.String(100), nullable=False)
    immigration_docs = db.Column('IMMIGRATION_DOCS', db.String(100), nullable=False)