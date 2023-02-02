from flask import Blueprint, render_template, redirect, url_for
from ..init_db import init_db

bp = Blueprint('bp_example', __name__)


@bp.route('/')
def example_get():
    init_db()
    return render_template('base.html')
