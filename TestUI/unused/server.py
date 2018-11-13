# -*- coding: utf-8 -*-

# Script to run from system:
#   python server.py

import socket
import sys
PORT_NUMBER = 5000
SIZE = 4096


def main():
    HOST = '0.0.0.0'
    
    mySocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    mySocket.bind( ("", PORT_NUMBER) )
    
    print ("Test server {0}:{1}\n".format(HOST,PORT_NUMBER))
    
    while True:
        data,addr = mySocket.recvfrom(SIZE)
        try: print(data)
        except: print('Error \n')
    mySocket.shutdown(socket.SHUT_RDWR)
    mySocket.close()
    sys.exit()


if __name__ == "__main__":
    main()