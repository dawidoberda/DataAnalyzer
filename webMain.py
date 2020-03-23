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

hist = Histogram()

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/histogram", methods= ["GET", "POST"])
def histogram():
    if request.method == "POST":
        # if 'reportFile' not in request.files:
        #     flash('No file part')
        report_from_request = request.files["reportFile"]
        filename = secure_filename(report_from_request.filename)
        path_to_del = app.config['UPLOAD_FOLDER']
        file_list = []
        for file in os.listdir(path_to_del):
            file_list.append(file)
        print(file_list)
        for file in file_list:
            os.remove(os.path.join(path_to_del, file))
        report_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        report_from_request.save(report_path)
        report_exist = hist.read_csv(report_path)
        print(report_exist)
        #return redirect(url_for('histogram'))
        return render_template('histogram.html')
    else:
        return render_template('histogram.html')
#TODO: histogram przerobiony na klase. teraz trzeba zrobic aby ta klase obslugiwalo sie z web
#TODO: przerobic wszystkie printy na log

#TODO: to dziwnie dziala jak sie wywola najpierw przycisk a pozniej sie chce wczytac plik to sie wysypuje. chyba nie moze tak byc. mnoze sprobowac zrobic tak aby przycisk byl linkiem do miejsca w tym html i tam dac kod?
@app.route('/dataLoad')
def SomeFunction():
    print('In SomeFunction')
    return render_template('histogram.html')

@app.route("/about")
def about():
    return render_template('about.html')


if __name__=="__main__":
    app.run(debug=True)