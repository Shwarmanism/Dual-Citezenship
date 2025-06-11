from app import db
from app.models import Applicant, FamilyMember, Overseas, Philippines, Child, SpouseDetails
import datetime
import traceback
import uuid

def submit_petition(form, user_id):
    try:
        action = form.get("action")
        print("Action received:", action)

        # --- Philippine Citizenship ---
        ph_citizenship_id = f"PH-{uuid.uuid4().hex[:8]}"
        mode = form.get("mode_ph_acquisition")
        if mode == "Others:":
            mode = form.get("mode_ph_acquisition_others") or "Others"

        philippines = Philippines(
            ph_citizenship_id=ph_citizenship_id,
            mode_ph_acquisition=mode,
            ph_docs=form.get('ph_docs')
        )
        db.session.add(philippines)
        db.session.flush()

        # --- Applicant ---
        applicant_name = form.get('applicant_name')
        print("Applicant Name:", applicant_name)

        has_alternative_name = form.get('has_alternative_name') == 'yes'
        alternative_name = form.get('alternative_name') if has_alternative_name else None
        alt_name_docs = form.getlist('applicant_supporting_docs[]')
        applicant_supporting_docs = ", ".join(alt_name_docs)

        db_raw = form.get('db_raw')
        applicant_DB = datetime.datetime.strptime(db_raw, "%Y-%m-%d").date() if db_raw else None

        applicant_cs = form.get('applicant_cs')
        if applicant_cs == "OTHERS":
            applicant_cs = form.get('civil_status_others') or "OTHERS"

        applicant = Applicant(
            id_no=user_id,
            applicant_name=applicant_name,
            alternative_name=alternative_name,
            applicant_supporting_docs=applicant_supporting_docs,
            applicant_DB=applicant_DB,
            applicant_PB=form.get('applicant_PB'),
            applicant_gender=form.get('applicant_gender'),
            applicant_cs=applicant_cs,
            ph_add=form.get('ph_add'),
            ph_residence=form.get('ph_residence'),
            home_telephone_no=form.get('home_telephone_no'),
            applicant_email=form.get('applicant_email'),
            applicant_occupation=form.get('applicant_occupation'),
            work_tl_no=form.get('work_tl_No'),
            work_address=form.get('work_address'),
            ph_citizenship_id=ph_citizenship_id
        )

        db.session.add(applicant)
        db.session.flush()
        entry_no = applicant.entry_no
        print("Generated Entry No:", entry_no)

        # --- Family Members ---
        relation_default = ["Father", "Mother", "Spouse"]
        for i in range(3):
            relation = form.get(f'relation_{i}', relation_default[i])

            spouse_id = f"S-{uuid.uuid4().hex[:8]}" if relation.lower() == 'spouse' else None

            family_member = FamilyMember(
                entry_no=entry_no,
                family_id=f"F-{i+1}",
                spouse_id=spouse_id,
                relation=relation,
                family_name=form.get(f'family_name_{i}'),
                citizenship=form.get(f'citizenship_{i}')
            )
            db.session.add(family_member)

            if relation.lower() == 'spouse':
                spouse_detail = SpouseDetails(
                    spouse_id=spouse_id,
                    spouse_address=form.get(f'spouse_address_{i}') or ''
                )
                db.session.add(spouse_detail)


        # --- Overseas Citizenship ---
        no_of_citizenship = int(form.get('no_of_citizenship', 0))

        foreign_citizenships = form.getlist("applicant_foreign_citizenship[]")
        modes_of_acquisition = form.getlist("mode_of_acquisition[]")
        date_of_acquisition_raw = form.getlist("date_of_acquisition[]")
        natural_cert_numbers = form.getlist("natural_cert_numbers[]")
        foreign_passport_nos = form.getlist("foreign_passport_no[]")
        date_of_issuance_raw = form.getlist("raw_issuance[]")
        places_of_issuance = form.getlist("place_of_issuance[]")
        foreign_docs = form.getlist("foreign_docs[]")

        for i in range(no_of_citizenship):
            date_of_acquisition = (
                datetime.datetime.strptime(date_of_acquisition_raw[i], "%Y-%m-%d").date()
                if date_of_acquisition_raw[i] else None
            )
            date_of_issuance = (
                datetime.datetime.strptime(date_of_issuance_raw[i], "%Y-%m-%d").date()
                if date_of_issuance_raw[i] else None
            )
            overseas = Overseas(
                entry_no=entry_no,
                overseas_id=f"FC-{i+1}",
                applicant_foreign_citizenship=foreign_citizenships[i],
                mode_of_acquisition=modes_of_acquisition[i],
                date_of_acquisition=date_of_acquisition,
                natural_cert_numbers=natural_cert_numbers[i],
                foreign_passport_no=foreign_passport_nos[i],
                date_of_issuance=date_of_issuance,
                place_of_issuance=places_of_issuance[i],
                foreign_docs=foreign_docs[i]
            )
            db.session.add(overseas)

        # --- Children ---
        if form.get('child_petition') == 'on':
            no_of_child_included = int(form.get('no_of_child_included', 0))

            for i in range(no_of_child_included):
                idx = i + 1  # Child numbering starts at 1

                child_name = form.getlist("child_name[]")[i] if form.getlist("child_name[]") else None
                dob_str = form.getlist("child_dob[]")[i] if form.getlist("child_dob[]") else None
                child_DB = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

                child_gender = form.get(f"child_gender_{idx}")
                child_cs = form.get(f"child_status_{idx}")
                child_cs_other = form.getlist("child_status_other[]")[i] if form.getlist("child_status_other[]") else None
                child_PB = form.getlist("child_birthplace[]")[i] if form.getlist("child_birthplace[]") else None
                child_citizenship = form.getlist("child_citizenship[]")[i] if form.getlist("child_citizenship[]") else None
                child_country = form.getlist("child_residence[]")[i] if form.getlist("child_residence[]") else None
                child_docs = form.getlist(f"child_docs_{idx}[]")
                child_immigration = form.getlist("child_immigration_docs[]")[i] if form.getlist("child_immigration_docs[]") else None

                final_civil_status = child_cs
                if child_cs == 'O' and child_cs_other:
                    final_civil_status = f"Others: {child_cs_other}"

                child = Child(
                    entry_no=entry_no,
                    child_id=f"C-{idx}",
                    child_name=child_name,
                    gender=child_gender,
                    civil_status=final_civil_status,
                    child_DB=child_DB,
                    child_PB=child_PB,
                    country_pa=child_country,
                    child_citizenship=child_citizenship,
                    child_supporting_docs=', '.join(child_docs),
                    immigration_docs=child_immigration
                )
                db.session.add(child)



        # --- Final Commit ---
        if action == "submit":
            db.session.commit()
            print("Form committed successfully.")
            return True, "Petition submitted successfully."
        else:
            db.session.rollback()
            print("Form not committed. Action was not 'submit'.")
            return False, f"Invalid action: '{action}'. Petition not submitted."

    except Exception as e:
        db.session.rollback()
        print("Exception occurred:", str(e))
        traceback.print_exc()
        return False, f"Error submitting petition: {str(e)}"
