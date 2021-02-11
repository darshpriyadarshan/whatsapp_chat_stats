from src.helpers.dates import Dates
from src.friend import Friend
from src.main import Main
import traceback
from flask import session, url_for, redirect, render_template, after_this_request, Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import os
import logging
SECRET_KEY = 'mysecretkey'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(413)
def too_large(e):
    logging.exception("File too large exception")
    return "File is too large", 413


@app.route('/stats', methods=['GET'])
def stats():
    try:
        logging.info("stats route::enter")
        main_obj = Main()
        file_handle = open(session['filename'], encoding="utf8", mode="r")
        main_obj.file_contents = file_handle.read()
        friend1 = Friend()
        friend2 = Friend()
        date_object = Dates()
        main_obj.prepare_stats(friend1, friend2, date_object)
        @after_this_request
        def remove_file(response):
            try:
                logging.debug("remove_file::enter")
                file_handle.close()
                os.remove(session['filename'])
                logging.debug("remove_file::exit")
            except Exception as error:
                app.logger.error(
                    "Error removing or closing downloaded file handle", error)
            return response
        logging.info("stats route::exit")
        return render_template("stats.html", main_obj=main_obj, friend1=friend1, friend2=friend2, date_object=date_object)
    except Exception as e:
        logging.exception("Exception in stats route handler")

class UploadForm(FlaskForm):
    file = FileField()


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        logging.info("upload route::enter")
        form = UploadForm()
        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    return "Not a valid file, .txt is expected", 400
                session['filename'] = filename
                form.file.data.save(filename)
                logging.info("upload route [POST]::exit")
                return redirect(url_for('stats'))
        logging.info("upload route [GET]::exit")
        return render_template('upload.html', form=form)
    except Exception as e:
        logging.exception("Exception in upload route handler")


@app.route('/')
def index():
    return render_template('index.html')



