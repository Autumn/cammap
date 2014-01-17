from flask import request, Response, render_template
from backend import app
from backend.database import db_session, engine
from sqlalchemy import text
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
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def subbed():
    error = None
    image = request.form.get('upload', None)
    radius = request.form.get('est_rad', None)
    location = request.form.get('loc_string', None)
    comment = request.form.get('comm', None)
    # TODO: Important GExiv2 stuff here
    sub = Submission(None, date.today(), 0, 0, 15, location, comment)
    db_session.add(sub)
    db_session.commit()
    return 'Submission accepted'

@app.route('/nearest')
def nearest():
    lati = request.args.get('lati', '')
    longi = request.args.get('longi', '')
    radius = 100000
    query = text("select * from test where earth_box(ll_to_earth(:lati, :longi), :radius) @> ll_to_earth(lati, longi)")
    res = engine.execute(query, lati=lati, longi=longi, radius=radius)
    print res.fetchall()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
