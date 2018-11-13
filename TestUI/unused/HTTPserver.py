# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global running
        if self.path == '/':
            self.list_files()
        elif self.path.startswith('/calculation'):
            self.send_calculation()
        elif self.path.startswith('/animate'):
            self.animate()
        elif self.path.startswith('/quit'):
            self.send_response(200)
            running = False
        else:
            self.send_file(self.path[1:])

    def do_POST(self):
        filename = self.path[1:] # Remove the / from the path
        filesize = int(self.headers['Content-Length'])
        contents = self.rfile.read(filesize)

        with open(filename, 'w') as f:
            f.write(contents.decode())

        self.send_response(200)

    def send_file(self, filename):
        # Check to see if file exists and is a file, not directory
        if os.path.isfile(filename):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()

            # Read and send the contents of the file
            with open(filename) as f:
                contents = f.read()
            self.wfile.write(contents.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(('Dude! File not found').encode('utf-8'))
            
    def animate(self):
        empty, operation, motor_cfg, anim_data = self.path.split('/')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        msg = "Received"
        self.wfile.write(msg.encode('utf-8'))
        
    def send_calculation(self):
        empty, operation, number1, number2 = self.path.split('/')
        result = str(int(number1) + int(number2))
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def list_files(self):
        file_list = os.listdir(os.curdir)
        if file_list:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            for filename in file_list:
                self.wfile.write(('{}\n'.format(filename)).encode('utf-8'))

#
# Main
#
running = True
server = HTTPServer(('', 9000), MyHandler)
print('Server started on host:{}, port:{}'.format(*server.server_address))
while running:
    server.handle_request()