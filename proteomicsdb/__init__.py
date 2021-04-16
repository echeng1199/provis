# application factory -- pulls all parts of our app together as a package

import os
from flask import Flask
from os.path import join, dirname, realpath
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)

    # set configuration, i.e. specify the parameters to direct the behavior of app at runtime
    app.config.from_mapping(
        SECRET_KEY='thesis',
        DATABASE=os.path.join(app.instance_path, 'proteomicsdb.sqlite'),  # where SQLite database file will be saved
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)  # configure with config.py file if it exists
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # directory on computer for uploading [currently not in use]
    app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/uploads')

    # register blueprints (modules) with application
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import help
    app.register_blueprint(help.bp)

    from . import posts
    app.register_blueprint(posts.bp)

    from . import search
    app.register_blueprint(search.bp)
    app.add_url_rule('/', endpoint='search.search')  # basically http://127.0.0.1:5000/

    from . import analysis
    app.register_blueprint(analysis.bp)

    return app


if __name__ == '__main__':
    app.run(debug=True)
