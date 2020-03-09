from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__) #tworzymy instancje klasy Flask

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/histogram")
def histogram():
    return render_template('histogram.html')

@app.route("/about")
def about():
    return render_template('about.html')


if __name__=="__main__":
    app.run(debug=True)