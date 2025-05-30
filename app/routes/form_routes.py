from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User, Applicant, Child, FamilyMember, Overseas, Philippines, SpouseDetails
from flask_login import login_required, current_user
import datetime

bp_form = Blueprint('form', __name__)

@bp_form.route("/petition", methods=["GET", "POST"])
@login_required
def petition():
    if request.method == "POST":
        try:
            # --- Applicant ---
            applicant_name = request.form.get('applicant_name')
            has_alternative_name = request.form.get('has_alternative_name') == 'on'
            alternative_name = request.form.get('alternative_name') if has_alternative_name else None
            db_raw = request.form.get('date_of_birth')
            applicant_DB = datetime.datetime.strptime(db_raw, "%Y-%m-%d").date() if db_raw else None
            applicant_PB = request.form.get('applicant_PB')
            applicant_gender = request.form.get('applicant_gender')
            applicant_cs = request.form.get('applicant_cs')
            ph_add = request.form.get('ph_add')
            ph_residence = request.form.get('ph_residence')
            applicant_mobile_no = request.form.get('mobile_no')
            applicant_email = request.form.get('applicant_email')
            applicant_occupation = request.form.get('applicant_occupation')
            work_address = request.form.get('work_address')
            applicant_supporting_docs = request.form.get('applicant_supporting_docs')

            applicant = Applicant(
                user_id=current_user.id_no,
                applicant_name=applicant_name,
                alternative_name=alternative_name,
                applicant_supporting_docs=applicant_supporting_docs,
                applicant_DB=applicant_DB,
                applicant_PB=applicant_PB,
                applicant_gender=applicant_gender,
                applicant_cs=applicant_cs,
                ph_add=ph_add,
                ph_residence=ph_residence,
                applicant_mobile_no=applicant_mobile_no,
                applicant_email=applicant_email,
                applicant_occupation=applicant_occupation,
                work_address=work_address
            )

            db.session.add(applicant)
            db.session.flush()  # Get the assigned entry_no
            entry_no = applicant.entry_no

            # --- Family Members ---
            family_members_data = request.form.getlist('family_members') 

            for idx, member_data in enumerate(family_members_data, start=1):
                family_id = f"F-{idx}"
                family_member = FamilyMember(
                    entry_no=entry_no,
                    family_id=family_id,
                    relation=member_data['relation'],
                    family_name=member_data['family_name'],
                    citizenship=member_data['citizenship']
                )
                db.session.add(family_member)

                # Handle spouse details if relation is "Spouse"
                if member_data['relation'].lower() == "spouse":
                    spouse_address = member_data.get('spouse_address')
                    spouse_id = "S-1"
                    spouse_detail = SpouseDetails(
                        family_id=family_id,
                        spouse_id=spouse_id,
                        spouse_address=spouse_address
                    )
                    db.session.add(spouse_detail)

            # --- Overseas Citizenship ---
            applicant_foreign_citizenship = request.form.get('applicant_foreign_citizenship')
            mode_of_acquisition = request.form.get('mode_of_acquisition')
            date_of_acquisition_raw = request.form.get('date_of_acquisition')
            date_of_acquisition = datetime.datetime.strptime(date_of_acquisition_raw, "%Y-%m-%d").date() if date_of_acquisition_raw else None
            natural_cert_numbers = request.form.get('natural_cert_numbers')
            foreign_passport_no = request.form.get('foreign_passport_no')
            issuance_of_foreign_passport = request.form.get('issuance_of_foreign_passport')
            place_of_issuance = request.form.get('supporting_documents_former')
            foreign_docs = request.form.get('supporting_documents_current')

            no_of_citizenship = int(request.form.get('no_of_citizenship', 0))
            for i in range(no_of_citizenship):
                overseas_id = f"FC-{i+1}"
                overseas = Overseas(
                    entry_no=entry_no,
                    overseas_id=overseas_id,
                    applicant_foreign_citizenship=applicant_foreign_citizenship,
                    mode_of_acquisition=mode_of_acquisition,
                    date_of_acquisition=date_of_acquisition,
                    natural_cert_numbers=natural_cert_numbers,
                    foreign_passport_no=foreign_passport_no,
                    issuance_of_foreign_passport=issuance_of_foreign_passport,
                    place_of_issuance=place_of_issuance,
                    foreign_docs=foreign_docs
                )
                db.session.add(overseas)

            # --- Philippine Citizenship ---
            ph_mode_of_acquisition = request.form.get('ph_mode_of_acquisition')
            ph_docs = request.form.get('ph_docs')

            philippines = Philippines(
                ph_id="PH-1",
                entry_no=entry_no,
                ph_mode_of_acquisition=ph_mode_of_acquisition,
                ph_docs=ph_docs
            )
            db.session.add(philippines)

            # --- Children ---
            child_petition = request.form.get('child_petition')
            if child_petition == 'on':
                no_of_child_included = int(request.form.get('no_of_child_included', 0))
                for i in range(no_of_child_included):
                    dob_child_raw = request.form.get(f'dob_child_{i}')
                    child_DB = datetime.datetime.strptime(dob_child_raw, "%Y-%m-%d").date() if dob_child_raw else None
                    child = Child(
                        entry_no=entry_no,
                        child_id=f"C-{i+1}",
                        child_name=request.form.get(f'child_name_{i}'),
                        child_gender=request.form.get(f'child_gender_{i}'),
                        child_csa=request.form.get(f'child_cs_{i}'),
                        child_DB=child_DB,
                        child_PB=request.form.get(f'child_PB_{i}'),
                        child_country_pa=request.form.get(f'child_country_pa_{i}'),
                        child_citizenship=request.form.get(f'child_citizenship_{i}'),
                        child_supporting_docs=request.form.get(f'child_supporting_docs_{i}'),
                        child_immagration_docs=request.form.get(f'child_immgration_docs_{i}')
                    )
                    db.session.add(child)

            db.session.commit()
            flash("Petition submitted successfully.", "success")
            return redirect(url_for("form.petition"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error submitting petition: {str(e)}", "danger")
            return redirect(url_for("form.petition"))

    return render_template("petition.html")
