# -*- coding: utf-8 -*-
#This will return an error as the server closes too quickly and doesn't
# timeout correctly
import urllib
import json

def make_url(server, port, path, scheme='http'):
    netloc = '{}:{}'.format(server, port)
    url = urllib.parse.urlunsplit((scheme, netloc, path, '', ''))
    return url

#
# Main
#
server = '192.168.2.8'
port = 9000

try: 
    # 1 - Request directory listing
    #url = make_url(server, port, '/')
    #file_list = urllib.request.urlopen(url).read()
    #print('Files from server:')
    #for filename in file_list.splitlines():
    #    print('- {}'.format(filename.decode('utf-8')))
    
    
    # 2 - Upload a file to the server. 
    #This writes correctly but may return an error.
    #contents = 'hello, world.\nThe End'
    #filename = 'foo.txt'
    #url = make_url(server, port, filename)
    #f = urllib.request.urlopen(url, data=contents.encode('utf-8'))
    
    
    # 3 - Request contents of a file
    #filename = input('Type a file name: ')
    #url = make_url(server, port, filename)
    #contents = urllib.request.urlopen(url).read()
    #print('Contents:')
    #print(contents)
    
    # 4 - Do some calculation
    #n1 = 19
    #n2 = 5
    #path = '/calculation/{}/{}'.format(n1, n2)
    #url = make_url(server, port, path)
    #result = urllib.request.urlopen(url).read()
    #print('{} + {} = {}'.format(n1, n2, result.decode('utf-8')))
    
    # 5 - send motor.cfg and anim.dat files
    motor_cfg = 'data//motor.cfg'
    path = '/animate/{}/{}'.format(motor_cfg,anim_data)
    url = make_url(server,port,path)
    result = urllib.request.urlopen(url).read()
    print(result.decode('utf-8'))
    
    # Send quit signal
    url = make_url(server, port, '/quit')
    urllib.request.urlopen(url).read()


except urllib.error.HTTPError as e:
    print(e.code)
except urllib.error.URLError as e:
    print("Host not found.")
except:
    print('\n Error \n')