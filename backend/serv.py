from flask import request, Response, render_template
from backend import app
from backend.database import db_session 
from backend.models import Submission
from datetime import date
from threading import Lock

import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

id_lock = Lock()
cur_id = Submission.query.order_by(Submission.id.desc()).first().id

@app.route('/')
def homepage():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/test')
def test():
    print "Current max key is: %d" % cur_id
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def subbed():
    global cur_id
    global id_lock
    error = None

    id_lock.acquire()
    cur_id += 1
    myid=cur_id
    id_lock.release()

    image = request.form.get('upload', None)
    radius = request.form.get('est_rad', None)
    location = request.form.get('loc_string', None)
    comment = request.form.get('comm', None)
    lati = request.form.get('lati', None)
    longi = request.form.get('longi', None)
    # TODO: Important GExiv2 stuff here
    sub = Submission(myid, datetime.datetime.now(), lati, longi, 15, location, comment)
    db_session.add(sub)
    db_session.commit()
    return 'Submission accepted'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
