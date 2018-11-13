# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os


app = Flask(__name__)
app.tempvar = ['Uhhh...']
basedir = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def ini():
    return 'Nothing here...'

@app.route("/animate", methods=['GET','POST'])
def animate():
    
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        app.tempvar = data
        return 'Received!'
    else:
        return str(app.tempvar)

@app.route('/copy_sounds', methods=['GET','POST'])
def copy_sounds():
    if os.path.exists(basedir + '\\sounds') == False:
        os.makedirs(basedir+'/sounds')
    app.config['UPLOAD_PATH'] = 'sounds/'
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            print(file)
            file.save(os.path.join(basedir,'\\sounds\\',file.filename))
        return 'Upload Complete'
    if request.method == 'GET':
        return jsonify({'Path': basedir+'\\sounds\\' ,'Sounds': os.listdir(basedir+'\\sounds\\')})
            
    

if __name__ == "__main__":
    app.run('0.0.0.0',9000)