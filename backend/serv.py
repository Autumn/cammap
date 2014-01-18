from flask import request, Response, render_template
from backend import app
from backend.database import db_session, engine
from sqlalchemy import text
from backend.models import Submission
from datetime import date
from threading import Lock
from werkzeug import secure_filename
from PIL import Image

import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
filestore = '/tmp/photos/keep'
tmpfiledir = '/tmp/photos/'

max_size = (640, 480)
thumb_size = (128,128)

id_lock = Lock()
id = Submission.query.order_by(Submission.id.desc()).first()
print id
if id == None:
    cur_id = 1
else:
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

    image = request.files['upload']
    image_fn = secure_filename(image.filename)
    saved_fn = os.path.join(tmpfiledir, "%d.jpg" % myid)

    # Save temporary file
    image.save(saved_fn)
    image.close()

    im = Image.open(saved_fn)
    print im.format
    if im.format == 'JPEG':
        # TODO: Catch exception when this fails
        im.verify()
        # Need to reopen after verify
        im = Image.open(saved_fn)
        im.thumbnail(max_size, Image.ANTIALIAS)
        im.save(os.path.join(filestore, "%d.jpg" % myid))
        im.thumbnail(thumb_size, Image.ANTIALIAS)
        im.save(os.path.join(filestore, "%d_thumb.jpg" % myid))
    else:
        return "Not a JPEG buddy", 400

    # Delete temporary file
    os.remove(saved_fn)

    # TODO: Important GExiv2 stuff here

    radius = request.form.get('est_rad', None)
    location = request.form.get('loc_string', None)
    comment = request.form.get('comm', None)
    lati = request.form.get('lati', None)
    longi = request.form.get('longi', None)
    sub = Submission(myid, datetime.datetime.now(), lati, longi, 15, location, comment)
    db_session.add(sub)
    db_session.commit()
    return 'Submission accepted'

@app.route('/image')
def imageget():
    id = request.args.get('id', '')
    try:
        exists = os.path.exists(filestore + "%d.jpg" % id)
    except IOError:
        return 'Image does not exist', 404
    if exists:
        return send_from_directory(filestore, "%d.jpg" % id)

@app.route('/nearest')
def nearest():
    lati = request.args.get('lati', '')
    longi = request.args.get('longi', '')
    radius = 100000
    query = text("select * from submissions where earth_box(ll_to_earth(:lati, :longi), :radius) @> ll_to_earth(lati, longi)")
    res = engine.execute(query, lati=lati, longi=longi, radius=radius)
    print res.fetchall()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
