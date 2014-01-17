from flask import request, Response, render_template
from backend import app
from backend.database import db_session 
from backend.models import Submission
from datetime import date

import os
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def homepage():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/test')
def test():
    return 'Test success!'

@app.route('/submit', methods=['POST'])
def submit(posted):
    error = None
    image = request.form['upload']
    radius = request.form['est_rad']
    location = request.form['loc_string']
    comment = request.form['comm']
    # TODO: Important GExiv2 stuff here
    sub = Submission(None, date.today(), 0, 0, 15, location, comment)
    return 'Submission accepted'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
