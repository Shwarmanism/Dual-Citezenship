from app import db
from app.models import Applicant, FamilyMember, Overseas, Philippines, Child, SpouseDetails, UserFunction
from datetime import datetime
import traceback
import uuid

def submit_petition(form, user_id, entry_no=None, editing=False):
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
        ph_docs = form.getlist('ph_docs[]')

        others_input = form.get('ph_docs_others', '').strip()
        if "OTHERS:" in ph_docs or "OTHERS" in ph_docs:
            ph_docs = [doc for doc in ph_docs if not doc.startswith("OTHERS")]
            if others_input:
                ph_docs.append(f"OTHERS: {others_input}")
        philippines.ph_docs = ", ".join(ph_docs)


        # --- Update Applicant ---
        applicant.applicant_name = form.get('applicant_name')
        
        has_alternative_name = form.get('has_alternative_name') == 'yes'
        applicant.alternative_name = form.get('alternative_name') if has_alternative_name else None
        alt_name_docs = form.getlist('applicant_supporting_docs[]')
        if alt_name_docs:
            if "Others" in alt_name_docs or "OTHERS" in alt_name_docs:
                others_input = form.get('applicant_supporting_docs_others', '').strip()
                if others_input:
                    alt_name_docs = [doc for doc in alt_name_docs if doc.lower() != "others"]
                    alt_name_docs.append(f"Others: {others_input}")
            applicant.applicant_supporting_docs = ", ".join(alt_name_docs)

        db_raw = form.get('db_raw')
        applicant.applicant_DB = datetime.strptime(db_raw, "%Y-%m-%d").date() if db_raw else None

        applicant_cs = form.get('applicant_cs')
        if applicant_cs == "OTHERS":
            applicant_cs = form.get('civil_status_others') or "OTHERS"
        applicant.applicant_cs = applicant_cs

        applicant.applicant_PB = form.get('applicant_PB')
        applicant.applicant_gender = form.get('applicant_gender')
        applicant.philippine_address = form.get('philippine_address')
        applicant.ph_residence = form.get('ph_residence')
        applicant.home_telephone_no = form.get('home_telephone_no')
        applicant.applicant_email = form.get('applicant_email')
        applicant.applicant_occupation = form.get('applicant_occupation')
        applicant.work_tl_no = form.get('work_tl_no')
        applicant.work_address = form.get('work_address')

        # --- Update Family Members ---
        existing_family = {
            f.relation.lower(): f for f in FamilyMember.query.filter_by(entry_no=entry_no).all()
        }
        existing_spouse_details = {
            f.spouse_id: f.spouse_details for f in existing_family.values()
            if f.relation.lower() == 'spouse' and f.spouse_id
        }

        relation_default = ["Father", "Mother", "Spouse"]

        for i in range(3):
            relation = form.get(f'relation_{i}', relation_default[i])
            family_name = form.get(f'family_name_{i}', '')
            citizenship = form.get(f'citizenship_{i}', '')
            relation_key = relation.lower()

            if relation_key in existing_family:
                family_member = existing_family[relation_key]
                family_member.family_name = family_name
                family_member.citizenship = citizenship
                db.session.add(family_member)

                if relation_key == 'spouse':
                    spouse_id = family_member.spouse_id
                    spouse_address = form.get(f'spouse_address_{i}', '')
                    if spouse_id and spouse_id in existing_spouse_details:
                        existing_spouse_details[spouse_id].spouse_address = spouse_address
                        db.session.add(existing_spouse_details[spouse_id])

        # --- Update Overseas ---
        existing_overseas = Overseas.query.filter_by(entry_no=entry_no).all()
        no_of_citizenship = int(form.get('no_of_citizenship') or 0)

        for i in range(no_of_citizenship):
            if i < len(existing_overseas):
                overseas = existing_overseas[i]
            else:
                overseas = Overseas(entry_no=entry_no, foreign_id=f"FC-{uuid.uuid4().hex[:8]}")
                db.session.add(overseas) 

            overseas.applicant_foreign_citizenship = form.getlist("applicant_foreign_citizenship[]")[i]
            overseas.acquisition_foreign_citizenship = form.getlist("acquisition_foreign_citizenship[]")[i]

            date_acquisition_raw = form.getlist("date_acquisition[]")[i]
            overseas.date_acquisition = datetime.strptime(date_acquisition_raw, "%Y-%m-%d").date()

            overseas.naturalization_no = form.getlist("naturalization_no[]")[i]
            overseas.foreign_passport_no = form.getlist("foreign_passport_no[]")[i]

            date_issuance_raw = form.getlist("date_issuance[]")[i]
            overseas.date_issuance = datetime.strptime(date_issuance_raw, "%Y-%m-%d").date() if date_issuance_raw else None

            overseas.place_issuance = form.getlist("place_issuance[]")[i]
            overseas.foreign_supporting_docs = form.getlist("foreign_supporting_docs[]")[i]


        # --- Update Children ---
        if form.get('child_button') == 'on':
            child_ids = form.getlist("child_id[]")
            child_names = form.getlist("child_name[]")
            child_dobs = form.getlist("child_dob[]")
            child_birthplaces = form.getlist("child_birthplace[]")
            child_citizenships = form.getlist("child_citizenship[]")
            child_residences = form.getlist("child_residence[]")
            child_immigration_docs = form.getlist("child_immigration_docs[]")
            child_status_others = form.getlist("child_status_other[]")

            no_of_child_included = len(child_names)

            for i in range(no_of_child_included):
                idx = i + 1
                dob_str = child_dobs[i] if child_dobs else None
                child_BD = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

                child_id = child_ids[i] if i < len(child_ids) else None
                child_gender = form.get(f"child_gender_{idx}")
                child_cs = form.get(f"child_status_{idx}")
                child_cs_other = child_status_others[i] if child_status_others else None

                final_civil_status = f"Others: {child_cs_other}" if child_cs == 'O' and child_cs_other else child_cs

                if not child_gender:
                    return False, f"Missing gender for child #{idx}."

                if not final_civil_status:
                    return False, f"Missing civil status for child #{idx}."

                if child_id:
                        child = Child.query.filter_by(entry_no=entry_no, child_id=child_id).first()
                        if child:
                            child.child_name = child_names[i]
                            child.child_gender = child_gender
                            child.child_civil_status = final_civil_status
                            child.child_BD = child_BD
                            child.child_PB = child_birthplaces[i]
                            child.country_pa = child_residences[i]
                            child.child_citizenship = child_citizenships[i]
                            child.child_supporting_docs = ', '.join(form.getlist(f"child_docs_{idx}[]"))
                            child.immigration_docs = child_immigration_docs[i]
                        else:
                            new_child = Child(
                                entry_no=entry_no,
                                child_id=child_id,
                                child_name=child_names[i],
                                child_gender=child_gender,
                                child_civil_status=final_civil_status,
                                child_BD=child_BD,
                                child_PB=child_birthplaces[i],
                                country_pa=child_residences[i],
                                child_citizenship=child_citizenships[i],
                                child_supporting_docs=', '.join(form.getlist(f"child_docs_{idx}[]")),
                                immigration_docs=child_immigration_docs[i]
                            )
                            db.session.add(new_child)
                else:
                        new_child = Child(
                            entry_no=entry_no,
                            child_id=f"C-{uuid.uuid4().hex[:8]}",
                            child_name=child_names[i],
                            child_gender=child_gender,
                            child_civil_status=final_civil_status,
                            child_BD=child_BD,
                            child_PB=child_birthplaces[i],
                            country_pa=child_residences[i],
                            child_citizenship=child_citizenships[i],
                            child_supporting_docs=', '.join(form.getlist(f"child_docs_{idx}[]")),
                            immigration_docs=child_immigration_docs[i]
                        )
                        db.session.add(new_child)

            user_func = UserFunction.query.get(entry_no)

            if user_func:
                user_func.location = applicant.philippine_address
                user_func.transaction = "Petition Update"
                user_func.status = "Active"
                user_func.date_updated = datetime.utcnow()
            else:
                user_func = UserFunction(
                        entry_no=entry_no,
                        location=applicant.philippine_address,
                        transaction="Petition Update",
                        status="Active",
                        created_at=applicant.created_at,
                        date_updated=datetime.utcnow()
                    )
                db.session.add(user_func)
        db.session.commit()
        return True, "Petition updated successfully."
    else:
        #New Entry
        try:
            action = form.get("action")
            print("Action received:", action)

            # --- Philippine Citizenship ---
            ph_citizenship_id = f"PH-{uuid.uuid4().hex[:8]}"

            ph_docs_list = form.getlist('ph_docs[]')

            ph_docs_others = form.get("ph_docs_others")
            if ph_docs_others:
                ph_docs_list.append(f"OTHERS: {ph_docs_others}")

            ph_docs_combined = "; ".join(ph_docs_list)
            mode = form.get("mode_ph_acquisition")
            if mode == "Others:":
                mode = form.get("mode_ph_acquisition_others") or "Others"

            philippines = Philippines(
                ph_citizenship_id=ph_citizenship_id,
                mode_ph_acquisition=mode,
                ph_docs=ph_docs_combined
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
            applicant_DB = datetime.strptime(db_raw, "%Y-%m-%d").date() if db_raw else None

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
                philippine_address=form.get('philippine_address'),
                ph_residence=form.get('ph_residence'),
                home_telephone_no=form.get('home_telephone_no'),
                applicant_email=form.get('applicant_email'),
                applicant_occupation=form.get('applicant_occupation'),
                work_tl_no=form.get('work_tl_no'),
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
                family_name = form.get(f'family_name_{i}')

                if not family_name:
                    continue

                spouse_id = None
                if relation.lower() == 'spouse':
                    if family_name.strip():
                        spouse_id = f"S-{uuid.uuid4().hex[:8]}"
                    else:
                        relation = 'Spouse'

                family_member = FamilyMember(
                    entry_no=entry_no,
                    family_id=f"F-{i+1}",
                    spouse_id=spouse_id,
                    relation=relation,
                    family_name=family_name,
                    citizenship=form.get(f'citizenship_{i}')
                )
                db.session.add(family_member)

                if spouse_id:
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
                        datetime.strptime(date_acquisition_raw[i], "%Y-%m-%d").date()
                        if date_acquisition_raw[i] else None
                    )
                    
                    date_issuance = (
                        datetime.strptime(date_issuance_raw[i], "%Y-%m-%d").date()
                        if date_issuance_raw[i] else None
                    )

                    overseas = Overseas(
                        entry_no=entry_no,
                        foreign_id=f"FC-{uuid.uuid4().hex[:8]}",
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
                
                no_of_child_included_str = form.get('no_of_child_included', '').strip()
                no_of_child_included = int(no_of_child_included_str) if no_of_child_included_str else 0

                for i in range(no_of_child_included):
                    idx = i + 1 

                    child_name = form.getlist("child_name[]")[i] if form.getlist("child_name[]") else None
                    dob_str = form.getlist("child_dob[]")[i] if form.getlist("child_dob[]") else None
                    child_BD = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

                    child_gender = form.get(f"child_gender_{idx}")
                    child_cs= form.get(f"child_status_{idx}")
                    child_cs_other = form.getlist("child_status_other[]")[i] if form.getlist("child_status_other[]") else None
                    child_PB = form.getlist("child_birthplace[]")[i] if form.getlist("child_birthplace[]") else None
                    child_citizenship = form.getlist("child_citizenship[]")[i] if form.getlist("child_citizenship[]") else None
                    child_country = form.getlist("child_residence[]")[i] if form.getlist("child_residence[]") else None
                    child_docs = form.getlist(f"child_docs_{idx}[]")
                    child_immigration = form.getlist("child_immigration_docs[]")[i] if form.getlist("child_immigration_docs[]") else None

                    if not all([child_name, child_gender, child_cs, child_BD, child_PB, child_citizenship, child_country]):
                        continue
                    
                    final_civil_status = child_cs
                    if child_cs == 'O' and child_cs_other:
                        final_civil_status = f"Others: {child_cs_other}"

                    child = Child(
                        entry_no=entry_no,
                        child_id=f"C-{uuid.uuid4().hex[:8]}",
                        child_name=child_name,
                        child_gender=child_gender,
                        child_civil_status=final_civil_status,
                        child_BD=child_BD,
                        child_PB=child_PB,
                        country_pa=child_country,
                        child_citizenship=child_citizenship,
                        child_supporting_docs=', '.join(child_docs),
                        immigration_docs=child_immigration
                    )
                    db.session.add(child)

            #----User Function----
            user_func_existing = UserFunction.query.get(entry_no)
            if not user_func_existing:
                user_func = UserFunction(
                    entry_no=entry_no,
                    location=applicant.philippine_address,
                    transaction="Petition Submission",
                    status="Active",
                    created_at=datetime.utcnow(),
                    date_updated=None
                )
                db.session.add(user_func)
            else:
                print(f"[INFO] Skipping: UserFunction for entry_no={entry_no} already exists.")

            # --- Final Commit ---
            if action == "submit":
                db.session.commit()
                print("Form committed successfully.")
                print("Child count:", no_of_child_included)
                print("Child names:", form.getlist("child_name[]"))
                print("Foreign citizenships:", form.getlist("applicant_foreign_citizenship[]"))
                print("Attempting to insert entry_no:", entry_no)
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
