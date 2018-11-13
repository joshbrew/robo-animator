# -*- coding: utf-8

import sys
#import subprocess
import os

server_script = os.path.dirname(sys.argv[0]) + '\\server.py'

#Tests via system rather than IDE
os.system('python '+ server_script)
