from flask import request, Response, render_template
from backend import app
from backend.database import db_session, engine
from sqlalchemy import text
from datetime import date
from threading import Lock

import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

id_lock = Lock()
#id = Submission.query.order_by(Submission.id.desc()).first()

query = text("select id from submissions order by id desc")
id = engine.execute(query).first()
print id
if id == None:
    cur_id = 0
else:
    cur_id = res.first() #Submission.query.order_by(Submission.id.desc()).first().id

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
    query = text("insert into submissions values(:id, :date, :lati, :longi, :radius, :location, :comment )")
    engine.execute(query, id=myid, date=datetime.datetime.now(), lati=lati, longi=longi, radius=radius, location=location, comment=comment)
    
    return 'Submission accepted'

@app.route('/nearest')
def nearest():
    lati = request.args.get('lati', '0.0')
    longi = request.args.get('longi', '0.0')
    radius = 100000
    query = text("select * from submissions where earth_box(ll_to_earth(:lati, :longi), :radius) @> ll_to_earth(lati, longi)")
    res = engine.execute(query, lati=lati, longi=longi, radius=radius)
    print res.fetchall()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
