from flask import Flask, request, make_response, Response, stream_with_context
from flask_cors import CORS
from tifProcess.tifLoader import Manager
import json
import traceback
import os
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

@APP.route("/temp/ln", methods=['POST'])
def make_link():
    src = os.path.abspath("data/meshs")
    pths = request.get_json()
    for pth in pths['path']:
        os.symlink(src, pth)
    return {}

@APP.route("/download/mesh", methods=['GET'])
def get_download():
    url = request.args.get("pth")
    CHUNK_SIZE = 8192
    def read_file_chunks(url):
        with open(url, 'rb') as fd:
            while 1:
                buf = fd.read(CHUNK_SIZE)
                if buf:
                    yield buf
                else:
                    break
    try:
        return Response(
            stream_with_context(read_file_chunks(url)),
            headers={
                'Content-Disposition': f'attachment; filename={"123.ply"}'
            }
        )
    except FileNotFoundError:
        return {"message" : "invalid id"}


if __name__ == "__main__":
    # signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    Manager().load()
    APP.run(port=PORT) # Do not edit this port