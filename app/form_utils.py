from app import db
from app.models import Applicant, FamilyMember, Overseas, Philippines, Child, SpouseDetails
import datetime

def submit_petition(form, user_id):
    try:
        # --- Applicant ---
        applicant_name = form.get('applicant_name')
        has_alternative_name = form.get('has_alternative_name') == 'on'
        alternative_name = form.get('alternative_name') if has_alternative_name else None
        db_raw = form.get('date_of_birth')
        applicant_DB = datetime.datetime.strptime(db_raw, "%Y-%m-%d").date() if db_raw else None
        applicant_PB = form.get('applicant_PB')
        applicant_gender = form.get('applicant_gender')
        applicant_cs = form.get('applicant_cs')
        ph_add = form.get('ph_add')
        ph_residence = form.get('ph_residence')
        applicant_mobile_no = form.get('mobile_no')
        applicant_email = form.get('applicant_email')
        applicant_occupation = form.get('applicant_occupation')
        work_address = form.get('work_address')
        applicant_supporting_docs = form.get('applicant_supporting_docs')

        applicant = Applicant(
            user_id=user_id,
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
        db.session.flush()
        entry_no = applicant.entry_no

        i = 0
        relation = ["Father", "Mother", "Spouse"]
        # --- Family Members ---
        for i in range(3):
            relation = form.get(f'relation_{i}')
            family_name = form.get(f'family_name_{i}')
            citizenship = form.get(f'citizenship_{i}')
            family_id = f"F-{i+1}"
            spouse_id = f"S-{i+1}" if relation and relation.lower() == 'spouse' else None

            family_member = FamilyMember(
                entry_no=entry_no,
                family_id=family_id,
                spouse_id=spouse_id,
                relation=relation,
                family_name=family_name,
                citizenship=citizenship
            )
            db.session.add(family_member)

            if spouse_id:
                spouse_address = form.get(f'spouse_address_{i}')
                spouse_detail = SpouseDetails(
                    spouse_id=spouse_id,
                    spouse_address=spouse_address or ''
                )
                db.session.add(spouse_detail)

        action = form.get("action")

        # --- Overseas Citizenship ---
        no_of_citizenship = int(form.get('no_of_citizenship', 0))

        for i in range(no_of_citizenship):

            overseas_id = f"FC-{i+1}"
            applicant_foreign_citizenship = form.get(f'applicant_foreign_citizenship_{i}')
            mode_of_acquisition = form.get(f'mode_of_acquisition_{i}')
            date_raw = form.get(f'date_of_acquisition_{i}')
            date_of_acquisition = datetime.datetime.strptime(date_raw, "%Y-%m-%d").date() if date_raw else None
            natural_cert_numbers = form.get(f'natural_cert_numbers_{i}')
            foreign_passport_no = form.get(f'foreign_passport_no_{i}')
            raw_issuance = form.get(f'raw_issuance_{i}')
            issuance_of_foreign_passport = datetime.datetime.strptime(raw_issuance, "%Y-%m-%d").date() if raw_issuance else None
            place_of_issuance = form.get(f'place_of_issuance_{i}')
            foreign_docs = form.get(f'foreign_docs_{i}')

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

        # --- Philippine Citizenship ---
        ph_citizenship_id = "PH-1"
        ph_mode_of_acquisition = form.get('ph_mode_of_acquisition')
        ph_docs = form.get('ph_docs')

        philippines = Philippines(
            ph_citizenship_id=ph_citizenship_id,
            ph_mode_of_aquisition=ph_mode_of_acquisition,
            ph_docs=ph_docs
        )
        db.session.add(philippines)
        db.session.flush()

        applicant.ph_citizenship_id = ph_citizenship_id

        # --- Children ---
        child_petition = form.get('child_petition')
        if child_petition == 'on':
            no_of_child_included = int(form.get('no_of_child_included', 0))
            for i in range(no_of_child_included):
                    dob_child_raw = form.get(f'dob_child_{i}')
                    child_DB = datetime.datetime.strptime(dob_child_raw, "%Y-%m-%d").date() if dob_child_raw else None
                    child = Child(
                        entry_no=entry_no,
                        child_id=f"C-{i+1}",
                        child_name=form.get(f'child_name_{i}'),
                        gender=form.get(f'child_gender_{i}'),
                        civil_status=form.get(f'child_cs_{i}'),
                        child_DB=child_DB,
                        child_PB=form.get(f'child_PB_{i}'),
                        country_pa=form.get(f'child_country_pa_{i}'),
                        child_citizenship=form.get(f'child_citizenship_{i}'),
                        child_supporting_docs=form.get(f'child_supporting_docs_{i}'),
                        immigration_docs=form.get(f'child_immigration_docs_{i}')
                    )
                    db.session.add(child)

        db.session.commit()
        return True, "Petition submitted successfully."
    except Exception as e:
        db.session.rollback()
        return False, f"Error submitting petition: {str(e)}"
