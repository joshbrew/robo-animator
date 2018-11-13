# -*- coding: utf-8 -*-
"""
Simple template rendering demo.
Runs on port 5000
"""

from flask import Flask, request, redirect, url_for, render_template, jsonify
#from flask_pymongo import PyMongo
import os



app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))

#app.config['MONGO_DBNAME'] = 'db'
#app.config['MONGO_URI'] = 'mongodb://0.0.0.0:5001/db'
# 'mongodb://<USER>:<PASS>@HOST:PORT/DBNAME'

#mongo = PyMongo(app)

@app.route("/")
def ini():
    return 'Demo pages: /streamIO /animator /login, /success/name'

@app.route('/login',methods = ['POST', 'GET'])
def login():
   
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      return render_template('index.html')

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/animator', methods = ['POST','GET'])
def animator():
    return render_template('animator.html')

@app.route('/streamIO')
def streamIO():
    return render_template('streamIO.html')


if __name__ == "__main__":
    app.run('0.0.0.0',5000)
    
