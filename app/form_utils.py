from app import db
from app.models import Applicant, FamilyMember, Overseas, Philippines, Child, SpouseDetails
import datetime
import traceback
import uuid

def submit_petition(form, user_id, entry_no=None):
    if entry_no:
         # --- Update Philippine Citizenship ---
        applicant = Applicant.query.filter_by(entry_no=entry_no, id_no=user_id).first()
        if not applicant:
            return False, "Petition not found for update."

        philippines = Philippines.query.filter_by(ph_citizenship_id=applicant.ph_citizenship_id).first()
        if not philippines:
            return False, "Philippine citizenship record not found."

        mode = form.get("mode_ph_acquisition")
        if mode == "Others:":
            mode = form.get("mode_ph_acquisition_others") or "Others"

        philippines.mode_ph_acquisition = mode
        philippines.ph_docs = form.get('ph_docs')

        # --- Update Applicant ---
        applicant.applicant_name = form.get('applicant_name')
        has_alternative_name = form.get('has_alternative_name') == 'yes'
        applicant.alternative_name = form.get('alternative_name') if has_alternative_name else None
        alt_name_docs = form.getlist('applicant_supporting_docs[]')
        if "Others" in alt_name_docs or "OTHERS" in alt_name_docs:
            others_input = form.get('applicant_supporting_docs_others', '').strip()
            if others_input:
                alt_name_docs = [doc for doc in alt_name_docs if doc.lower() != "others"]
                alt_name_docs.append(f"Others: {others_input}")
        applicant.applicant_supporting_docs = ", ".join(alt_name_docs)

        db_raw = form.get('db_raw')
        applicant.applicant_DB = datetime.datetime.strptime(db_raw, "%Y-%m-%d").date() if db_raw else None

        applicant_cs = form.get('applicant_cs')
        if applicant_cs == "OTHERS":
            applicant_cs = form.get('civil_status_others') or "OTHERS"
        applicant.applicant_cs = applicant_cs

        applicant.applicant_PB = form.get('applicant_PB')
        applicant.applicant_gender = form.get('applicant_gender')
        applicant.ph_add = form.get('ph_add')
        applicant.ph_residence = form.get('ph_residence')
        applicant.home_telephone_no = form.get('home_telephone_no')
        applicant.applicant_email = form.get('applicant_email')
        applicant.applicant_occupation = form.get('applicant_occupation')
        applicant.work_tl_no = form.get('work_tl_No')
        applicant.work_address = form.get('work_address')

        # --- Update Family Members ---
        FamilyMember.query.filter_by(entry_no=entry_no).delete()
        SpouseDetails.query.filter(SpouseDetails.spouse_id.in_([
            f.spouse_id for f in FamilyMember.query.filter_by(entry_no=entry_no).all() if f.relation.lower() == 'spouse'])).delete()

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

        # --- Update Overseas ---
        Overseas.query.filter_by(entry_no=entry_no).delete()

        if form.get("citizenship_button") == "on":
            no_of_citizenship = int(form.get('no_of_citizenship', 0))
            for i in range(no_of_citizenship):
                date_acquisition = datetime.datetime.strptime(form.getlist("date_acquisition[]")[i], "%Y-%m-%d").date() if form.getlist("date_acquisition[]")[i] else None
                date_issuance = datetime.datetime.strptime(form.getlist("date_issuance[]")[i], "%Y-%m-%d").date() if form.getlist("date_issuance[]")[i] else None

                overseas = Overseas(
                    entry_no=entry_no,
                    foreign_id=f"FC-{i+1}",
                    applicant_foreign_citizenship=form.getlist("applicant_foreign_citizenship[]")[i],
                    acquisition_foreign_citizenship=form.getlist("acquisition_foreign_citizenship[]")[i],
                    date_acquisition=date_acquisition,
                    naturalization_no=form.getlist("naturalization_no[]")[i],
                    foreign_passport_no=form.getlist("foreign_passport_no[]")[i],
                    date_issuance=date_issuance,
                    place_issuance=form.getlist("place_issuance[]")[i],
                    foreign_supporting_docs=form.getlist("foreign_supporting_docs[]")[i]
                )
                db.session.add(overseas)

        # --- Update Children ---
        Child.query.filter_by(entry_no=entry_no).delete()

        if form.get('child_button') == 'on':
            no_of_child_included = int(form.get('no_of_child_included', 0))
            for i in range(no_of_child_included):
                idx = i + 1
                dob_str = form.getlist("child_dob[]")[i] if form.getlist("child_dob[]") else None
                child_BD = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
                child_cs = form.get(f"child_status_{idx}")
                child_cs_other = form.getlist("child_status_other[]")[i] if form.getlist("child_status_other[]") else None
                final_civil_status = f"Others: {child_cs_other}" if child_cs == 'O' and child_cs_other else child_cs

                child = Child(
                    entry_no=entry_no,
                    child_id=f"C-{idx}",
                    child_name=form.getlist("child_name[]")[i],
                    gender=form.get(f"child_gender_{idx}"),
                    civil_status=final_civil_status,
                    child_BD=child_BD,
                    child_PB=form.getlist("child_birthplace[]")[i],
                    country_pa=form.getlist("child_residence[]")[i],
                    child_citizenship=form.getlist("child_citizenship[]")[i],
                    child_supporting_docs=', '.join(form.getlist(f"child_docs_{idx}[]")),
                    immigration_docs=form.getlist("child_immigration_docs[]")[i]
                )
                db.session.add(child)

        db.session.commit()
        return True, "Petition updated successfully."
    else:
        #New Entry
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

            if "Others" in alt_name_docs or "OTHERS" in alt_name_docs:
                others_input = form.get('applicant_supporting_docs_others', '').strip()
                if others_input:
                    
                     alt_name_docs = [doc for doc in alt_name_docs if doc.lower() != "others"]
                     alt_name_docs.append(f"Others: {others_input}")

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
            if form.get("citizenship_button") == "on":
                no_of_citizenship = int(form.get('no_of_citizenship', 0))

                applicant_foreign_citizenship = form.getlist("applicant_foreign_citizenship[]")
                acquisition_foreign_citizenship = form.getlist("acquisition_foreign_citizenship[]")
                date_acquisition_raw = form.getlist("date_acquisition[]")
                naturalization_no = form.getlist("naturalization_no[]")
                foreign_passport_no = form.getlist("foreign_passport_no[]")
                date_issuance_raw = form.getlist("date_issuance[]")
                place_issuance = form.getlist("place_issuance[]")
                foreign_supporting_docs = form.getlist("foreign_supporting_docs[]")

                for i in range(no_of_citizenship):
                    date_acquisition = (
                            datetime.datetime.strptime(date_acquisition_raw[i], "%Y-%m-%d").date()
                            if date_acquisition_raw[i] else None
                        )
                    
                    date_issuance = (
                        datetime.datetime.strptime(date_issuance_raw[i], "%Y-%m-%d").date()
                        if date_issuance_raw[i] else None
                    )
                    overseas = Overseas(
                        entry_no=entry_no,
                        foreign_id=f"FC-{i+1}",
                        applicant_foreign_citizenship=applicant_foreign_citizenship[i],
                        acquisition_foreign_citizenship=acquisition_foreign_citizenship[i],
                        date_acquisition=date_acquisition,
                        naturalization_no=naturalization_no[i],
                        foreign_passport_no=foreign_passport_no[i],
                        date_issuance=date_issuance,
                        place_issuance=place_issuance[i],
                        foreign_supporting_docs=foreign_supporting_docs[i]
                    )
                    db.session.add(overseas)
                

            # --- Children ---
            if form.get('child_button') == 'on':
                no_of_child_included = int(form.get('no_of_child_included', 0))

                for i in range(no_of_child_included):
                    idx = i + 1  # Child numbering starts at 1

                    child_name = form.getlist("child_name[]")[i] if form.getlist("child_name[]") else None
                    dob_str = form.getlist("child_dob[]")[i] if form.getlist("child_dob[]") else None
                    child_BD = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

                    child_gender = form.get(f"child_gender_{idx}")
                    child_cs= form.get(f"child_status_{idx}")
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
                        child_BD=child_BD,
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
                print("Child count:", no_of_child_included)
                print("Child names:", form.getlist("child_name[]"))
                print("Foreign citizenships:", form.getlist("applicant_foreign_citizenship[]"))
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
