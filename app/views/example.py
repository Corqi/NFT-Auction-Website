from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('bp_example', __name__)


@bp.route('/')
def example_get():
    return render_template('base.html')
