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
    suffix = db.Column(db.String(7), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(18), nullable=False)

    petitions = db.relationship('Petition', backref='user', lazy=True)


class Petition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_no'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Personal info
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    # Optional alternative name info
    has_alternative_name = db.Column(db.Boolean, default=False)
    alternative_first_name = db.Column(db.String(50))
    alternative_middle_name = db.Column(db.String(50))
    alternative_last_name = db.Column(db.String(50))
    court_decree = db.Column(db.String(200))
    documents = db.Column(db.String(200))

    # Spouse info
    spouse_first_name = db.Column(db.String(50), nullable=False)
    spouse_middle_name = db.Column(db.String(50), nullable=False)
    spouse_last_name = db.Column(db.String(50), nullable=False)
    spouse_citizenship = db.Column(db.String(50), nullable=False)

    # Father
    father_first_name = db.Column(db.String(50), nullable=False)
    father_middle_name = db.Column(db.String(50), nullable=False)
    father_last_name = db.Column(db.String(50), nullable=False)
    father_citizenship = db.Column(db.String(50), nullable=False)

    # Mother
    mother_first_name = db.Column(db.String(50), nullable=False)
    mother_middle_name = db.Column(db.String(50), nullable=False)
    mother_last_name = db.Column(db.String(50), nullable=False)
    mother_citizenship = db.Column(db.String(50), nullable=False)

    # Foreign citizenship info
    applicant_foreign_citizenship = db.Column(db.String(50), nullable=False)
    mode_of_acquisition = db.Column(db.String(100), nullable=False)
    date_of_acquisition = db.Column(db.Date, nullable=False)
    natural_cert_numbers = db.Column(db.String(100), nullable=False)
    foreign_passport_no = db.Column(db.String(50), nullable=False)
    issuance_of_foreign_passport = db.Column(db.String(100), nullable=False)

    # Supporting documents
    supporting_documents_former = db.Column(db.String(200), nullable=False)
    supporting_documents_current = db.Column(db.String(200), nullable=False)

    # Contact info
    ph_permanent_add = db.Column(db.String(200), nullable=False)
    foreign_add = db.Column(db.String(200), nullable=False)
    mobile_no = db.Column(db.String(20), nullable=False)
    applicant_email = db.Column(db.String(100), nullable=False)
    work_address = db.Column(db.String(200), nullable=False)

    # Relationships
    overseas_citizenship = db.relationship('OverseasCitizenship', backref='petition', uselist=False)
    family_members = db.relationship('FamilyMember', backref='petition', lazy=True)
    spouse_details = db.relationship('SpouseDetails', backref='petition', uselist=False)
    philippine_citizenship = db.relationship('PhilippineCitizenship', backref='petition', uselist=False)
    children = db.relationship('PetitionChild', backref='petition', lazy=True, cascade="all, delete-orphan")


class PetitionChild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petition.id'), nullable=False)

    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    civil_status = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    pob = db.Column(db.String(100), nullable=False)
    citizenship = db.Column(db.String(50), nullable=False)
    perm_address = db.Column(db.String(100), nullable=False)
    supporting_docs = db.Column(db.String(200), nullable=False)
