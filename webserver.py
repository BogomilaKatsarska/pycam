import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
SERVER_PORT = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('index.html', 'r') as file:
            self.wfile.write(bytes(file.read(), 'utf-8'))


if __name__ == '__main__':
    p = subprocess.Popen(['python', '-u', 'websocket.py'])

    webserver = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print(f'Server started at http://{HOST_NAME}:{SERVER_PORT}')
    webserver.serve_forever()