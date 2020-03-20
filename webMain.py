from flask import Flask
from flask import render_template
from flask import url_for, redirect
from flask import request
from histogram import Histogram
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'C:/Users/oberdad/Desktop/Projects/DataAnalyzer/upload'
ALLOWED_EXTENSIONS = set(['xlsx', 'csv'])

app = Flask(__name__) #tworzymy instancje klasy Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/histogram", methods= ["GET", "POST"])
def histogram():
    hist = Histogram()
    if request.method == "POST":
        # if 'reportFile' not in request.files:
        #     flash('No file part')
        report_from_request = request.files["reportFile"]
        filename = secure_filename(report_from_request.filename)
        #TODO: usunac najpierw wszystko co jest w tym folderze i dopiero pozniej zapisac
        report_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        report_from_request.save(report_path)
        return redirect(url_for('histogram'))
    else:
        return render_template('histogram.html')
#TODO: histogram przerobiony na klase. teraz trzeba zrobic aby ta klase obslugiwalo sie z web

@app.route("/about")
def about():
    return render_template('about.html')


if __name__=="__main__":
    app.run(debug=True)