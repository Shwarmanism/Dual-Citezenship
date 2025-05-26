from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, logout_user, login_required
import datetime

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
            
            return redirect(url_for("bp_form.petition"))
        else:
            flash("Login failed. Check your email/password.", "anger")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        account_type = request.form.get('account_type')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        prefix = request.form.get('prefix')
        suffix = request.form.get('suffix')
        date_of_birth = request.form.get('date_of_birth')
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        contact_number = request.form.get('contact_number')
        
        email, password = verification()

        existing_user = User.queary.filter_by(User.email == email).first()
        if existing_user:
            flash("Username or email is already exist.", "anger")
            return redirect(url_for(auth.register))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user=User(
            account_type=account_type,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            prefix=prefix,
            suffix=suffix,
            date_of_birth=dob,
            contact_number=contact_number,
            email=email, 
            password=hashed_password)

        db.session.add(new_user)
        db.seesion.commut()

        flash("Registered Successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

def verification():
    email = request.form.get('email')
    verify_email = request.form.get('verify_email')

    if email != verify_email:
        flash("Email does not match!", "danger")
        return render_template("register.html", email=email, password=password)
            
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')

    if password != verify_password:
        flash("Password does not match!", "anger")
        return render_template("register.hmtl", email=email, password=password)
    
    return email, password
        
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))