import os
import glob
from flask import Flask, request, redirect, url_for, send_file
from werkzeug import secure_filename
from PyPDF2 import PdfFileMerger

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
html = open("./index.html","r").read()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    return html

@app.route("/upload/", methods=['POST'])
def upload():
    if request.method == 'POST':
      f = request.files['file']
      f.save((os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))))
    return (html + " <form <p>%s</p>"
      % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],)))


@app.route("/merge/", methods=['POST'])
def merge():
    pdfs = os.listdir("./uploads/")
    print(pdfs)
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append("./uploads/" + pdf)
    with open('./uploads/result.pdf', 'wb') as fout:
        merger.write(fout)
    return (html  + " <form <p>%s</p>"
      % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],)))

@app.route("/download/", methods=['GET'])
def download():
    return send_file('uploads/result.pdf',
                     mimetype='application/pdf',
                     attachment_filename='result.pdf',
                     as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
