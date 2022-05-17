import json

from puller import FramesCatalog
from marketing import marketing_recruiting
from data_base import data_base

URLS = {'/finolog': FramesCatalog().get_frames_json,
        '/marketing': marketing_recruiting,
        '/recruiting': marketing_recruiting}

POST_URLS = ['/webhooks/marketing', '/webhooks/recruiting']


def application(environ, start_response):
    headers = [('Content-type', 'application/json; charset=utf-8')]
    try:
        if not environ['REQUEST_METHOD'] == 'POST':
            current_handler = URLS[environ['PATH_INFO']]
            status = '200 OK'
            start_response(status, headers)
            response = [current_handler(data_base(environ)).encode()]
            if environ['PATH_INFO'] == '/finolog':
                response = [current_handler().encode()]
        elif environ['PATH_INFO'] in POST_URLS:
            status = '200 OK'
            start_response(status, headers)
            request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
            request_body_json = json.loads(request_body)
            data_base(environ, request_body_json)
            response = [json.dumps(request_body_json).encode()]
        else:
            status = '404 Not Found'
            start_response(status, headers)
            response = [json.dumps(dict(detail=status)).encode()]
    except:
        status = '404 Not Found'
        start_response(status, headers)
        response = [json.dumps(dict(detail=status)).encode()]
    return response
