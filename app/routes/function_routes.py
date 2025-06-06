from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required
from app.form_utils import submit_petition
from app.models import UserFunction, Applicant
from app import db

bp_function = Blueprint('function', __name__)

@bp_function.route('/user')
@login_required
def display_data():
    applications = (
        db.session.query(UserFunction)
        .join(Applicant)
        .filter(Applicant.user_id == current_user.id_no)
        .all()
    )
    return render_template("user.html", user_functions=applications)

@bp_function.route('/delete_entry/<int:entry_no>', methods=['POST'])
@login_required
def delete_entry(entry_no):

    applicant = Applicant.query.get(entry_no)
    if not applicant or applicant.user_id != current_user.id_no:
        return "Unauthorized or Not Found", 403

    try:
        user_func = UserFunction.query.get(entry_no)
        if user_func:
            db.session.delete(user_func)

        db.session.delete(applicant)
        db.session.commit()
        return redirect('/user')

    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}", 500

@bp_function.route("/resubmit/<int:entry_no>", methods=["POST"])
@login_required
def resubmit_application(entry_no):
    success, msg = submit_petition(request.form, current_user.id_no)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("function.display_data"))
