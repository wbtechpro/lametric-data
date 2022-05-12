from puller import FramesCatalog
import json

URLS = {'/finolog': FramesCatalog().get_frames_json}


def application(environ, start_response):
    headers = [('Content-type', 'application/json; charset=utf-8')]
    try:
        current_handler = URLS[environ['PATH_INFO']]
        status = '200 OK'
        start_response(status, headers)
        response = [current_handler().encode()]
    except:
        status = '404 Not Found'
        start_response(status, headers)
        response = [json.dumps(dict(detail=status)).encode()]
    return response
