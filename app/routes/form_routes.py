from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.form_utils import submit_petition
from app import db
from flask_login import login_required, current_user
import datetime

bp_form = Blueprint('form', __name__)


@bp_form.route("/petition", methods=["GET", "POST"])
@login_required
def petition():
    if request.method == "POST":
        success, msg = submit_petition(request.form, current_user.id_no)
        flash(msg, "success" if success else "danger")
        return redirect(url_for("form.petition"))
    return render_template("petition.html")
