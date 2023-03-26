from flask import Flask, request, make_response
from flask_cors import CORS
from tifProcess.tifLoader import Manager
import json
import traceback
"""
!!!
Make sure some mesh files are generated and do Manager().save() before running this server
TODO:
I will convert the Manager class into a database(sqlite or psql or whatever it is)
"""
PORT = 9999
def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = make_response()
    print('response', err, repr(err))
    response.data = json.dumps({
        "error sting": repr(err),
        "name": "System Error",
        "message": traceback.format_exc(),
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
    assert type(data['polygon']) is list
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
    Manager().load()
    APP.run(port=PORT) # Do not edit this port