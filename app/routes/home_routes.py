from flask import Blueprint, render_template

bp_home = Blueprint('home', __name__)

@bp_home.route('/')
def home_index():
    return render_template('homepage.html')

@bp_home.route('/about')
def about():
    return render_template('about.html')

@bp_home.route('/intro')
def intro():
    return render_template('intro.html')

@bp_home.route('/dataprivacynotice')
def dataprivacy():
    return render_template('dataprivacynotice.html')

@bp_home.route('/eservices')
def eservices():
    return render_template('eservices.html')

@bp_home.route('/visa')
def visa():
    return render_template('visa.html')