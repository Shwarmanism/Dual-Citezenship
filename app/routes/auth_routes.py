from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from database.config import mysql_path

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully", "success")
            
            return redirect(url_for("form.petition"))
        else:
            flash("Login failed. Check your email/password.", "anger")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()

        date_of_birth = form_data.get("date_of_birth", "").strip()

        print(f"[DEBUG] Raw date_of_birth = '{date_of_birth}'")

        if not date_of_birth:
            flash("Date of Birth is required.", "danger")
            return render_template("register.html", form=form_data)

        try:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            print(f"[DEBUG] Parsed DOB = {dob}")
        except Exception as e:
            print(f"[ERROR] Date parsing failed: {e}")
            flash("Invalid date format.", "danger")
            return render_template("register.html", form=form_data)


        email, password = verification()
        if not email or not password:
            return render_template("register.html", form=form_data)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists.", "danger")
            return render_template("register.html", form=form_data)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            account_type=form_data.get("account_type"),
            first_name=form_data.get("first_name"),
            middle_name=form_data.get("middle_name"),
            last_name=form_data.get("last_name"),
            prefix=form_data.get("prefix"),
            suffix=form_data.get("suffix"),
            user_gender=form_data.get("user_gender"),
            user_civil_status=form_data.get("user_civil_status"),
            user_citizenship=form_data.get("user_citizenship"),
            date_of_birth=dob,
            country_birth=form_data.get("country_birth"),
            contact_number=form_data.get("contact_number"),
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.flush()

        db.session.commit()

        flash("Registered successfully.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

def verification():
    email = request.form.get('email')
    verify_email = request.form.get('verify_email')
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')

    if email != verify_email:
        flash("Email addresses do not match.", "danger")
        return None, None

    if password != verify_password:
        flash("Passwords do not match.", "danger")
        return None, None

    return email, password

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))