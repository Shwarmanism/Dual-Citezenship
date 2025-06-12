from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required
from app.form_utils import submit_petition
from app.models import UserFunction, Applicant
from app import db

bp_function = Blueprint('function', __name__)

@bp_function.route('/Online_Verification')
@login_required
def display_data():

    limit = request.args.get('limit', default=None, type=int)
    
    query = (
    db.session.query(UserFunction)
    .join(Applicant)
    .filter(Applicant.id_no == current_user.id_no)
    )

    if limit:
        query = query.limit(limit)

    applications = query.all()

    return render_template("Online_Verification.html", user_functions=applications)

@bp_function.route('/delete/<int:entry_no>', methods=['POST'])
@login_required
def delete_entry(entry_no):
    applicant = Applicant.query.get(entry_no)

    if applicant:
        db.session.delete(applicant)
        db.session.commit()
        flash('Application and all related records deleted successfully.', 'success')
    else:
        flash('Entry not found.', 'danger')

    return redirect(url_for('function.display_data'))

