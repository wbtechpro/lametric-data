from http.server import BaseHTTPRequestHandler, HTTPServer

import settings
from puller import FramesCatalog


class MyBaseHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        response = FramesCatalog().get_frames_json()
        self.wfile.write(response.encode())


def run(server_class=HTTPServer, handler_class=MyBaseHTTPRequestHandler):
    server_address = (settings.HOST, settings.PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
