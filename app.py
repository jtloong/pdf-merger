import os, errno, glob, time, random, string, io
from flask import Flask, request, redirect, url_for, send_file, render_template, make_response,flash
from werkzeug import secure_filename
from PyPDF2 import PdfFileMerger
from datetime import datetime
import sqlite3 as sql


ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getUploadedFiles(user):
    con = sql.connect("database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM files WHERE (user =?)",(user,))
    filenames = []

    for row in data:
        filenames.append(dict(name=row[2]))

    cur.close()
    con.close()
    return filenames

@app.route("/", methods=['GET', 'POST'])
def index():
    user = id_generator()
    resp = make_response(render_template('index.html', title='Home'))
    resp.set_cookie('userID', user)

    return resp

@app.route("/upload/", methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            userID = str(request.cookies.get('userID'))
            time = str(datetime.now())
            f = request.files['file']
            currentFiles = []

            con = sql.connect("database.db")

            cur = con.cursor()

            print(f.filename)
            print(con)
            print(cur)
            print("User: " + userID + " | time of visit: " + time + "| file:" + f.filename)

            cur.execute("INSERT INTO files (user, timeOfVisit, filename,file) VALUES (?,?,?,?)",(userID,time, f.filename,f.read()))
            con.commit()
            print("Record successfully added")

            currentFiles = getUploadedFiles(userID)
            print(currentFiles)

            cur.close()
            con.close()
        except:
            print("error in insert operation")
            return render_template('index.html', file_names = currentFiles, title='Home')
        finally:
            return render_template('index.html', file_names = currentFiles, title='Home')




@app.route("/merge/", methods=['POST'])
def merge():
    con = sql.connect("database.db")
    cur = con.cursor()
    user = str(request.cookies.get('userID'))
    data = cur.execute("SELECT * FROM files WHERE (user =?)",(user,))
    pdfs = []
    merger = PdfFileMerger()
    for row in data:
        merger.append(io.BytesIO(row[3]))
    cur.close()
    con.close()
    with open('./downloads/result' + user + '.pdf', 'wb') as fout:
        merger.write(fout)
    return send_file('./downloads/result' + user + '.pdf',
                         mimetype='application/pdf',
                         attachment_filename='result.pdf',
                         as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
