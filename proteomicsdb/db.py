# database blueprint creates and initializes database for storing user information and uploads

import sqlite3  # use SQLite database to store users and their data/files
import click  # package for creating cmd line interfaces
# current_app = app handling the request, useful for accessing app w/o importing it
from flask import current_app, g # g stores globals that can be accessed throughout the application
from flask.cli import with_appcontext

from .make_index import clear_index


# Function: open connection to database
def get_db():
    if 'db' not in g:
        # open a connection to the SQLite database file
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


# Function: close database connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Function: initialize and create database
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Function: make cmd line argument that will initialize and clear database whenever called
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    clear_index()
    click.echo('Initialized the database.') # print this


# Function: register functions in this file with the application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
