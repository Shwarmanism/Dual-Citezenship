from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User, Petition, PetitionChild
from flask_login import login_user, logout_user, login_required, current_user
import datetime

bp_form = Blueprint('form', __name__)

@bp_form.route("/petition", methods=["GET", "POST"])
@login_required
def petition():
    if request.method == "POST":

        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        has_alternative_name = request.form.get('has_alternative_name')

        date_of_birth = request.form.get('date_of_birth')
        dob = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        alternative_first_name = alternative_middle_name = alternative_last_name = court_decree = documents = None

        if has_alternative_name:
            alternative_first_name = request.form.get('alternative_first_name')
            alternative_middle_name = request.form.get('alternative_middle_name')
            alternative_last_name = request.form.get('alternative_last_name')
            court_decree = request.form.get('court_decree')
            documents = request.form.get('documents')

        spouse_first_name = request.form.get('spouse_first_name')
        spouse_middle_name = request.form.get('spouse_middle_name')
        spouse_last_name = request.form.get('spouse_last_name')
        spouse_citizenship = request.form.get('citizenship_of_spouse')

        father_first_name = request.form.get('father_first_name')
        father_middle_name = request.form.get('father_middle_name')
        father_last_name = request.form.get('father_last_name')
        father_citizenship = request.form.get('citizenship_of_father')

        mother_first_name = request.form.get('mother_first_name')
        mother_middle_name = request.form.get('mother_middle_name')
        mother_last_name = request.form.get('mother_last_name')
        mother_citizenship = request.form.get('citizenship_of_mother')

        applicant_foreign_citizenship = request.form.get('applicant_foreign_citizenship')
        mode_of_acquisition = request.form.get('mode_of_acquisition')
        date_of_acquisition = request.form.get('date_of_acquisition')
        natural_cert_numbers = request.form.get('natural_cert_numbers')
        foreign_passport_no = request.form.get('foreign_passport_no')
        issuance_of_foreign_passport = request.form.get('issuance_of_foreign_passport')
        supporting_documents_former = request.form.get('supporting_documents_former')
        supporting_documents_current = request.form.get('supporting_documents_current')

        ph_permanent_add = request.form.get('ph_permanent_add')
        foreign_add = request.form.get('foreign_add')
        mobile_no = request.form.get('mobile_no')
        applicant_email = request.form.get('applicant_email')
        work_address = request.form.get('work_address')

        petition = Petition(
            user_id=current_user.id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            has_alternative_name=has_alternative_name,
            alternative_first_name=alternative_first_name,
            alternative_middle_name=alternative_middle_name,
            alternative_last_name=alternative_last_name,
            court_decree=court_decree,
            documents=documents,
            date_of_birth=dob,
            spouse_first_name=spouse_first_name,
            spouse_middle_name=spouse_middle_name,
            spouse_last_name=spouse_last_name,
            spouse_citizenship=spouse_citizenship,
            father_first_name=father_first_name,
            father_middle_name=father_middle_name,
            father_last_name=father_last_name,
            father_citizenship=father_citizenship,
            mother_first_name=mother_first_name,
            mother_middle_name=mother_middle_name,
            mother_last_name=mother_last_name,
            mother_citizenship=mother_citizenship,
            applicant_foreign_citizenship=applicant_foreign_citizenship,
            mode_of_acquisition=mode_of_acquisition,
            date_of_acquisition=date_of_acquisition,
            natural_cert_numbers=natural_cert_numbers,
            foreign_passport_no=foreign_passport_no,
            issuance_of_foreign_passport=issuance_of_foreign_passport,
            supporting_documents_former=supporting_documents_former,
            supporting_documents_current=supporting_documents_current,
            ph_permanent_add=ph_permanent_add,
            foreign_add=foreign_add,
            mobile_no=mobile_no,
            applicant_email=applicant_email,
            work_address=work_address
        )


        child_petition = request.form.get('child_petition')
        if child_petition:
            no_of_child_included = int(request.form.get('no_of_child_included'))
            
            for i in range(no_of_child_included):
                dob_child_raw = request.form.get(f'dob_child_{i}')
                dob_child = datetime.datetime.strptime(dob_child_raw, "%Y-%m-%d").date() if dob_child_raw else None

                child = PetitionChild(
                    first_name=request.form.get(f'child_first_name_{i}'),
                    middle_name=request.form.get(f'child_middle_name_{i}'),
                    last_name=request.form.get(f'child_last_name_{i}'),
                    gender=request.form.get(f'child_gender_{i}'),
                    civil_status=request.form.get(f'child_civil_{i}'),
                    dob=dob_child,
                    pob=request.form.get(f'pob_child_{i}'),
                    citizenship=request.form.get(f'countries_of_citizenship_child_{i}'),
                    perm_address=request.form.get(f'country_of_perm_add_{i}'),
                    supporting_docs=request.form.get(f'child_supporting_docs_{i}')
                )
                petition.children.append(child)

        
        db.session.add(petition)
        db.session.commit()

        flash("Petition submitted successfully.", "success")
        return redirect(url_for("form.petition"))

    return render_template("petition.html")