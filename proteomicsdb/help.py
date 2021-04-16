# help blueprint displays help information

from flask import (Blueprint, render_template)

bp = Blueprint('help', __name__)


# various help functions
@bp.route('/help', methods=('GET',))
def help():
    return render_template('help/help.html')


@bp.route('/help/about', methods=('GET',))
def about():
    return render_template('help/about.html')


@bp.route('/help/starting', methods=('GET',))
def starting():
    return render_template('help/starting.html')


@bp.route('/help/uploading', methods=('GET',))
def uploading():
    return render_template('help/uploading.html')


@bp.route('/help/searching', methods=('GET',))
def searching():
    return render_template('help/searching.html')


@bp.route('/help/faq', methods=('GET',))
def faq():
    return render_template('help/faq.html')


@bp.route('/help/api', methods=('GET',))
def api():
    return render_template('help/api.html')
