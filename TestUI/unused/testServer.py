# -*- coding: utf-8 -*-
"""

"""
import os 

bpath =  'C:\\Program Files\\Bforartists 096\\bforartists.exe'
server_script = 'C:\\Users\\crazy\\Documents\\TestUI\\blender_server.py'
PATH = 'C:\\Users\\crazy\\Documents\\TestUI\\'
# This only seems to work in background mode for blender.
# Also, make this is run in a separate console while the main one sends client scripts.
os.system('"'+bpath+'"'+' -b --python '+server_script)


# in second window, enter the command os.system('python '+PATH+'blender_client.py'+PATH+'openBlender_testServer.py')