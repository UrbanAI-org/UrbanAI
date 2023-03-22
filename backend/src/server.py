from flask import Flask, request, make_response
from flask_cors import CORS
from tifProcess.tifLoader import Manager
import json
PORT = 9999
def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

@APP.route("/query/mesh", methods=['POST'])
def get_meshs():
    data = request.get_json()
    ids = Manager().searchChunk(data['polygon'])
    urls = []
    for id in ids:
        url = Manager().getChunkSavedURL(id, ".ply")
        if url is None:
            continue
        urls.append(url)
    return json.dumps(urls)

if __name__ == "__main__":
    # signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=PORT) # Do not edit this port