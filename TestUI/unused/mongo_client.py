# -*- coding: utf-8 -*-
from flask import Flask
from flask_pymongo import PyMongo
#import urllib
#from pprint import pprint

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'robo'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/robo'

mongo = PyMongo(app)

@app.route('/ya')
def ya():
    data = mongo.db.data
    data.insert_one({'test':'case'})
    return str(data)

@app.route('/uhhuh')
def uhhuh():
    data = mongo.db.data
    cursor = data.find({})
    x = []

    for doc in cursor:
        x.append(str(doc))
        
    return str(x)

if __name__ == '__main__':
    app.run()