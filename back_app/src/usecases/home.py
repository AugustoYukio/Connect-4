from flask import Blueprint, render_template

bp_home = Blueprint('bp_home', __name__, url_prefix='/')


@bp_home.route('/')
def home():
    return render_template('index.html', )
