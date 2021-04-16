# authentication blueprint for logging in, registering, logging out, etc.

# views = function to respond to users' requests
# blueprint = group of related views + other code

import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from proteomicsdb.db import get_db

# add the url_prefix '/auth' to all the urls associated with 'auth' blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


# View: register
# GET requests data from server (i.e. display this on page), POST sends data from user to server (i.e. user input)
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # get registration info
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        affiliation = request.form['affiliation']

        db = get_db()
        error = None

        # validate information
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)  # get first same username, if any

        # save
        if error is None:
            db.execute('INSERT INTO user (first_name, last_name, email, username, password, affiliation) '
                       'VALUES (?, ?, ?, ?, ?, ?)',
                       (first_name, last_name, email, username, generate_password_hash(password), affiliation))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')  # register if not already registered


# View: login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'There is no account associated with this username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()  # session dict stores data info across requests
            session['user_id'] = user['id']
            return redirect(url_for('search.search'))

        flash(error)

    return render_template('auth/login.html')


# View: load user information if logged in
@bp.before_app_request  # run this function before anything else, no matter what url is requested
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:  # check if user id is stored in session and get the user's data
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()


# View: log out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('search.search'))


# View: check if user is logged in
# using decorator (below)
def login_required(view):  # take as an argument any view
    # whenever '@login_required' is specified, this code runs to ensure that the user is logged in to run that view
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
