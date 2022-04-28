from puller import FramesCatalog


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'application/json; charset=utf-8')]
    start_response(status, headers)
    response = FramesCatalog().get_frames_json()
    return [response.encode()]
