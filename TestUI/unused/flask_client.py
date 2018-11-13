# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
#url = 'http://localhost:9000/animate'

#json1 = json.load(open('data//motor.cfg'))
#json2 = json.load(open('data//data.dat'))
#jsondat = [json1,json2]

#requests.post(url, json=jsondat)


url = 'http://localhost:9000/copy_sounds'
files = [('file', open('sounds//h2g2-freeze.wav', 'rb')),('file', open('sounds//h2g2-tears.wav', 'rb'))]
print(files)
r = requests.post(url, files=files)

print(r.text)