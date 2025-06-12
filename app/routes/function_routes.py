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
        .all()
    )
    
    if limit:
        query = query.limit(limit)

    applications = query.all()

    return render_template("Online_Verification.html", user_functions=applications)

@bp_function.route('/delete/<int:entry_no>', methods=['POST'])
def delete_entry(entry_no):
    user_function = UserFunction.query.get(entry_no)
    if user_function:
        db.session.delete(user_function)
        db.session.commit()
        flash('Entry deleted successfully.', 'success')
    else:
        flash('Entry not found.', 'danger')
    return redirect(url_for('function.display_verification'))

@bp_function.route("/resubmit/<int:entry_no>", methods=["POST"])
@login_required
def resubmit_application(entry_no):
    success, msg = submit_petition(request.form, current_user.id_no)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("function.display_data"))
