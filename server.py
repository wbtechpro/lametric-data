from wsgiref.simple_server import make_server

import settings
from puller import FramesCatalog


def my_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=utf-8')]
    start_response(status, headers)
    response = FramesCatalog().get_frames_json()

    return [response.encode()]


if __name__ == '__main__':
    with make_server(settings.HOST, settings.PORT, my_app) as srv:
        srv.serve_forever()
