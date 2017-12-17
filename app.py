import os, errno, glob
from flask import Flask, request, redirect, url_for, send_file, render_template
from werkzeug import secure_filename
from PyPDF2 import PdfFileMerger
import sqlite3 as sql

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png'])
userIP = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.before_request
def getSessionID():
    userIP = request.remote_addr

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        os.makedirs("./uploads")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return render_template('index.html', title='Home')

@app.route("/upload/", methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            f = request.files['file']
            print(f.filename)
            con = sql.connect("database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO files (user,filename,file) VALUES (?,?,?,?)",(userIP,secure_filename(f.filename),f) )
            con.commit()
            print("Record successfully added")
        except:
            con.rollback()
            print("error in insert operation")
        finally:
            return render_template('index.html', title='Home')
            con.close()



@app.route("/merge/", methods=['POST'])
def merge():
    pdfs = os.listdir("./uploads/")
    print(pdfs)
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append("./uploads/" + pdf)
    with open('./uploads/result.pdf', 'wb') as fout:
        merger.write(fout)
    return render_template('index.html', title='Home')

@app.route("/download/", methods=['GET'])
def download():
    return send_file('uploads/result.pdf',
                     mimetype='application/pdf',
                     attachment_filename='result.pdf',
                     as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
