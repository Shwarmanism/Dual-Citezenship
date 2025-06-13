from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.form_utils import submit_petition
from app.models import UserFunction, Applicant, Philippines, FamilyMember, Overseas, Child
from app import db
from flask_login import login_required, current_user
from datetime import datetime

bp_form = Blueprint('form', __name__)

@bp_form.route("/petition", methods=["GET", "POST"])
@login_required
def petition():
    if request.method == "POST":
        success, msg = submit_petition(request.form, current_user.id_no)
        
        if success:
            applicant = Applicant.query.filter_by(id_no=current_user.id_no).first()
            if applicant:
                flash("Petition submitted and tracked successfully!", "success")
            else:
                flash("Applicant record not found.", "danger")
        else:
            flash(msg, "danger")

        return redirect(url_for("function.display_data"))

    # GET method: just render the form
    return render_template("petition.html", editing=False, applicant=None, philippine=None)


@bp_form.route("/edit/<int:entry_no>", methods=["GET", "POST"])
@login_required
def edit_petition(entry_no):
    # --- Fetch existing applicant record ---
    applicant = Applicant.query.filter_by(entry_no=entry_no, id_no=current_user.id_no).first()

    if not applicant:
        flash("Petition not found.", "danger")
        return redirect(url_for("function.display_data"))

    if request.method == "POST":
        success, msg = submit_petition(request.form, current_user.id_no, entry_no=entry_no, editing=True)

        if success:
            flash("Petition updated and tracked successfully.", "success")
        else:
            flash(f"Failed to update petition: {msg}", "danger")

        return redirect(url_for("function.display_data"))

    entry_no=applicant.entry_no
    philippine=applicant.philippine

    supporting_docs = applicant.applicant_supporting_docs.split(", ") if applicant.applicant_supporting_docs else []
    others_text = ""
    for doc in supporting_docs:
        if doc.lower().startswith("others:"):
            others_text = doc.split(":", 1)[1].strip()
            break
    
    family_members = FamilyMember.query.filter_by(entry_no=entry_no).all()
    overseas_list = Overseas.query.filter_by(entry_no=entry_no).all()
    children = Child.query.filter_by(entry_no=entry_no).all()

    return render_template(
    "petition.html",
    applicant=applicant,
    philippine=philippine,
    editing=True,
    entry_no=entry_no,
    supporting_docs=supporting_docs,
    others_text=others_text,
    family_members=family_members,
    overseas_list=overseas_list,
    children=children
    )


