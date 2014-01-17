from flask import request, Response, render_template
from backend import app
from backend.database import db_session

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('basedir', 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

@app.route('/')
def homepage():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/test')
def test():
    return 'Test success!'

@app.route('/submit')
def submit(posted):
    return 'Submission not implemented yet'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
