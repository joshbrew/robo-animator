# -*- coding: utf-8 -*-

# Run this through the system commandline with desired scripts after running server.py
#  python client.py script1.py script2.py

import sys
import json
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SHUT_RDWR

SERVER_IP   = '192.168.2.9'
PORT_NUMBER = 5000
SIZE = 4096

mySocket = socket( AF_INET, SOCK_DGRAM )
myMessage = json.load(open('data//data.dat'))
myMessage1 = str(myMessage[0])
#print(myMessage[0])
try:
    mySocket.connect((SERVER_IP,PORT_NUMBER))
    print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))
    
    #mySocket.sendall(sys.argv[2].encode('utf-8') + b'\x00')
    mySocket.sendall(myMessage1.encode('utf-8'))
    mySocket.shutdown(SHUT_RDWR)
    mySocket.close()
except: print('Error')
finally: 
    print('Done')
    
