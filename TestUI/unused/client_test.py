# -*- coding: utf-8 -*-
"""

"""

import os
import sys
import subprocess



client_script = os.path.dirname(sys.argv[0]) + '\\client.py'
test_script = os.path.dirname(sys.argv[0]) + '\\test.py'

proc = subprocess.Popen(['python',client_script,test_script], stdout=subprocess.PIPE)
out = proc.communicate()[0].decode('utf-8')
print(out)