from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User, Applicant, Child, FamilyMember, Overseas, Philippines, SpouseDetails
from flask_login import login_required, current_user
import datetime
from database.config import mysql_path

bp_form = Blueprint('form', __name__)

@bp_form.route("/petition", methods=["GET", "POST"])
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
                work_address=work_address,
                ph_citizenship_id=None
            )

            db.session.add(applicant)
            db.session.flush()  # Get the assigned entry_no
            entry_no = applicant.entry_no

            # --- Family Members ---
            no_of_family_members = int(request.form.get('no_of_family_members', 0))
            for i in range(no_of_family_members):
                relation = request.form.get(f'relation_{i}')
                family_name = request.form.get(f'family_name_{i}')
                citizenship = request.form.get(f'citizenship_{i}')
                family_id = f"F-{i+1}"
                spouse_id = None

                # If relation is spouse, generate spouse_id
                if relation and relation.lower() == 'spouse':
                    spouse_id = f"S-{i+1}"
                else:
                    spouse_id = None

                family_member = FamilyMember(
                    entry_no=entry_no,
                    family_id=family_id,
                    spouse_id=spouse_id,
                    relation=relation,
                    family_name=family_name,
                    citizenship=citizenship
                )
                db.session.add(family_member)

                # If spouse, add spouse details
                if spouse_id:
                    spouse_address = request.form.get(f'spouse_address_{i}')
                    spouse_detail = SpouseDetails(
                        spouse_id=spouse_id,
                        spouse_address=spouse_address or ''
                    )
                    db.session.add(spouse_detail)

            # --- Overseas Citizenship ---
            no_of_citizenship = int(request.form.get('no_of_citizenship', 0))
            for i in range(no_of_citizenship):
                overseas_id = f"FC-{i+1}"
                applicant_foreign_citizenship = request.form.get(f'applicant_foreign_citizenship_{i}')
                mode_of_acquisition = request.form.get(f'mode_of_acquisition_{i}')
                date_of_acquisition_raw = request.form.get(f'date_of_acquisition_{i}')
                date_of_acquisition = datetime.datetime.strptime(date_of_acquisition_raw, "%Y-%m-%d").date() if date_of_acquisition_raw else None
                natural_cert_numbers = request.form.get(f'natural_cert_numbers_{i}')
                foreign_passport_no = request.form.get(f'foreign_passport_no_{i}')
                issuance_of_foreign_passport = request.form.get(f'issuance_of_foreign_passport_{i}')
                place_of_issuance = request.form.get(f'place_of_issuance_{i}')
                foreign_docs = request.form.get(f'foreign_docs_{i}')

                overseas = Overseas(
                    entry_no=entry_no,
                    overseas_id=overseas_id,
                    applicant_foreign_citizenship=applicant_foreign_citizenship,
                    mode_of_acquisition=mode_of_acquisition,
                    date_of_acquisition=date_of_acquisition,
                    natural_cert_numbers=natural_cert_numbers,
                    foreign_passport_no=foreign_passport_no,
                    date_of_issuance=issuance_of_foreign_passport,
                    place_of_issuance=place_of_issuance,
                    foreign_docs=foreign_docs
                )
                db.session.add(overseas)
                db.session.flush()

            # --- Philippine Citizenship ---
            ph_citizenship_id = "PH-1"  # Or generate as you want
            ph_mode_of_acquisition = request.form.get('ph_mode_of_acquisition')
            ph_docs = request.form.get('ph_docs')

            philippines = Philippines(
                ph_citizenship_id=ph_citizenship_id,
                ph_mode_of_aquisition=ph_mode_of_acquisition,
                ph_docs=ph_docs
            )
            
            db.session.add(philippines)
            db.session.flush()

            applicant.ph_citizenship_id=ph_citizenship_id
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
                        gender=request.form.get(f'child_gender_{i}'),
                        civil_status=request.form.get(f'child_cs_{i}'),
                        child_DB=child_DB,
                        child_PB=request.form.get(f'child_PB_{i}'),
                        country_pa=request.form.get(f'child_country_pa_{i}'),
                        child_citizenship=request.form.get(f'child_citizenship_{i}'),
                        child_supporting_docs=request.form.get(f'child_supporting_docs_{i}'),
                        immigration_docs=request.form.get(f'child_immigration_docs_{i}')
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
