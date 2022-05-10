from puller import FramesCatalog


def test():
    return '111'


URLS = {'/finolog': FramesCatalog().get_frames_json}


def application(environ, start_response):
    headers = [('Content-type', 'application/json; charset=utf-8')]
    try:
        current_handler = URLS[environ['PATH_INFO']]
        status = '200 OK'
        start_response(status, headers)
    except KeyError:
        status = '404 Not Found'
        start_response(status, headers)
        return
    return [current_handler().encode()]
