import os, errno, glob, time, random, string, io
from flask import Flask, request, redirect, url_for, send_file, render_template, make_response
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


@app.route("/", methods=['GET', 'POST'])
def index():
    user = id_generator()

    resp = make_response(render_template('index.html', title='Home'))
    resp.set_cookie('userID', user)
    print(user)

    return resp

@app.route("/upload/", methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            print("Hello?")
            userID = str(request.cookies.get('userID'))
            print(userID)
            time = str(datetime.now())
            print(time)
            f = request.files['file']

            con = sql.connect("database.db")
            cur = con.cursor()

            print(f.filename)
            print(con)
            print(cur)
            print("User: " + userID + " | time of visit: " + time + "| file:" + f.filename)

            cur.execute("INSERT INTO files (user, timeOfVisit, filename,file) VALUES (?,?,?,?)",(userID,time, f.filename,f.read()))
            con.commit()
            print("Record successfully added")

            cur.close()
            con.close()
        except:
            print("error in insert operation")
            return render_template('index.html', title='Home')
        finally:
            return render_template('index.html', title='Home')




@app.route("/merge/", methods=['POST'])
def merge():
    con = sql.connect("database.db")
    cur = con.cursor()
    user = str(request.cookies.get('userID'))
    data = cur.execute("SELECT * FROM files WHERE (user =?)",(user,))
    pdfs = []
    merger = PdfFileMerger()
    for row in data:
        print("User: " + row[0] + " | time of visit: " + row[1] + "| file:" + row[2])
        merger.append(io.BytesIO(row[3]))

    with open('./downloads/result.pdf', 'wb') as fout:
        merger.write(fout)
    return send_file('downloads/result.pdf',
                         mimetype='application/pdf',
                         attachment_filename='result.pdf',
                         as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
