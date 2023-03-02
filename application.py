from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin




application = Flask(__name__)
app = application

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/course_list", methods = ['GET','POST'])
def index():
    return 'page construnction in progress'
