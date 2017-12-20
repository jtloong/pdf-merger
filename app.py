import os, errno, glob, time
from flask import Flask, request, redirect, url_for, send_file, render_template
from werkzeug import secure_filename
from PyPDF2 import PdfFileMerger
import sqlite3 as sql

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf'])
userIP = ""
timeOfVisit = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        os.makedirs("./downloads")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print(userIP + " - " + timeOfVisit)
    return render_template('index.html', title='Home')

@app.route("/upload/", methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            userIP = str(request.remote_addr)
            f = request.files['file']
            print(f.filename)
            con = sql.connect("database.db")
            print(con)
            cur = con.cursor()
            print(cur)
            print("User: " + userIP + " | time of visit: " + str(time.asctime(time.localtime(time.time()))) + "| file:" + f.filename)
            cur.execute("INSERT INTO files (user, timeOfVisit, filename,file) VALUES (?,?,?,?)",(userIP,timeOfVisit, f.filename,f.read()))
            con.commit()
            print("Record successfully added")
            cur.close()
            con.close()
        except Exception as e:
            print("error in insert operation: " + e)
            return render_template('index.html', title='Home')
        finally:
            return render_template('index.html', title='Home')




@app.route("/merge/", methods=['POST'])
def merge():
    con = sql.connect("database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM files WHERE user =? AND timeOfVisit=?",(userIP))
    pdfs = []
    # while True:
    #
    #     rows = cur.fetchall()
    #     for row in rows:
    #         if row == None:
    #             break
    #         print (row[2])
    #

    # print(pdfs)
    # merger = PdfFileMerger()
    # for pdf in pdfs:
    #     merger.append(pdf)
    # with open('./uploads/result.pdf', 'wb') as fout:
    #     merger.write(fout)
    return render_template('index.html', title='Home')

@app.route("/download/", methods=['GET'])
def download():
    return send_file('downloads/result.pdf',
                     mimetype='application/pdf',
                     attachment_filename='result.pdf',
                     as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
