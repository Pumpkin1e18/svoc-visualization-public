# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask import request
import analyzer

app = Flask(__name__)

cnt = 0

#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/")
def hello():
    return render_template('index.html')

#「/templates」へアクセスがあった場合に、index.htmlを返す
@app.route("/templates", methods=["GET"])
def index():
    return render_template("index.html")


#「/nextpage」へアクセスがあった場合に、brat.htmlを返す
@app.route("/nextpage", methods=["GET"])
def nextpage():
    print('1')
    global cnt
    print('2')
    cnt = cnt+1
    print('3')
    html_name = 'output' + str(cnt) + '.html'
    print('4')
    output_file_name = 'templates/' + html_name
    original_text = request.args["Sentence"]
    analyzer.analyze(original_text, output_file_name)
    return render_template(html_name)



# @app.route('/')
# def index():
# 	return render_template('index.html')

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5001)
