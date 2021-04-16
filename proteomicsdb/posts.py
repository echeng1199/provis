# posts blueprint creates and displays users' post information

import os
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, Response, current_app)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import pandas as pd
import io

from resources import get_bucket, get_bucket_list, get_s3_client
from proteomicsdb.auth import login_required
from proteomicsdb.db import get_db
from .make_index import format_file, make_dict, create_schema, create_index, remove_doc

bp = Blueprint('posts', __name__)


# Function: get all posts in database (regardless of the user)
def all_posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, created, author_id, description, file_name, username, species, condition, timept'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return posts


# Function: get post

# removed ", check_author=True"
def get_post(id):
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, created, author_id, description, file_name, username, species, condition, timept'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    # if check_author and post['author_id'] != g.user['id']:
    #    abort(403)

    return post


# View: display index to show all uploads/posts
@bp.route('/database')
def index():
    return render_template('posts/index.html', posts=all_posts())


# View: create posts
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        filename = secure_filename(file.filename)

        species = request.form['species']
        condition = request.form['condition']
        timept = request.form['timept']

        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)

        if file:  # if there's a file save it
            # save info in SQL database
            db = get_db()
            db.execute(
                'INSERT INTO post (title, author_id, description, file_name, species, condition, timept)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (title, g.user['id'], description, filename, species, condition, timept)
            )
            db.commit()

            postid = str(db.execute(
                'SELECT seq from sqlite_sequence WHERE name = "post"'
            ).fetchone()['seq'])

            # save file on Amazon S3
            my_bucket = get_bucket()
            my_bucket.Object(file.filename).put(Body=file)
            flash("File uploaded successfully! Entries added to index!")

            # make Whoosh index for file
            bucket = "proteomics-db-test"
            file_df = format_file(get_df(bucket, filename))
            file_dict = make_dict(file_df)
            num_proteins = len(file_df)


            # not a great way to pass condition like this, because any
            # modification to post will not be accepted by Whoosh
            create_index(postid, condition, file_dict, create_schema(), num_proteins)

            return redirect(url_for('posts.index'))

    return render_template('posts/create.html')


# View: update post
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        species = request.form['species']
        condition = request.form['condition']
        timept = request.form['timept']

        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, description = ?, species = ?, condition = ?, timept = ?'
                ' WHERE id = ?',
                (title, description, species, condition, timept, id)
            )
            db.commit()
            return redirect(url_for('posts.index'))

    return render_template('posts/update.html', post=post)


# View: delete post and remove associated contents from Whoosh index
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    # remove from SQL database
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()

    key = request.form['key']
    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    # remove file contents from Whoosh index
    remove_doc(str(id))

    flash('File deleted successfully! Contents removed from index!')

    return redirect(url_for('posts.index'))


# View: download file from S3
@bp.route('/download', methods=('POST',))
def download():
    key = request.form['key']
    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={'Content-Disposition': 'attachment;filename={}'.format(key)}
    )


# Function: get file from S3 and return as df
def get_df(bucket_name, filename):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket_name, Key=filename)
    df = pd.read_excel(io.BytesIO(obj['Body'].read()))  # 'Body' is a key word
    return df


# View: view post contents on separate page
@bp.route('/<int:id>/view_post')
def view_post(id):
    post = get_post(id)
    return render_template("posts/view_post.html", post=post)
