from flask import Flask, request, make_response, Response, stream_with_context
# from flask_cors import CORS
from flask_restx import Api, Resource, fields, inputs, reqparse
# from flask_restx import 
# from tifProcess.tifLoader import Manager
import json
import traceback
import os
import time

"""
!!!
Make sure some mesh files are generated and do Manager().save() before running this server
TODO:
I will convert the Manager class into a database(sqlite or psql or whatever it is)
"""
PORT = 9999


app = Flask(__name__)
API = Api(app)
# APP.config['TRAP_HTTP_EXCEPTIONS'] = True
# APP.register_error_handler(Exception, defaultHandler)
chunk_id = "153370ea-07a4-4f96-a0d7-d7650111ab66"
# chunk_id = "abc"
mesh_resource_id = "4aa5660c-bff0-472d-bc66-0868a1477acf"
mesh_resource_id = "4aa5660c-bff0-472d-bc66-0868a1477acf"
pcd_resource_id = "b16be8bf-4c0d-4898-9a63-f683f9f2cb7a"
pcd_resource_id = "b16be8bf-4c0d-4898-9a63-f683f9f2cb7a"
@API.route("/v1/query/chunks")
class V1QueryChunks(Resource):
    def get(self):
        
        return {
            'geo-origin' : [-33.5, 151.5],
            "resources" : [
                {
                    "id" : chunk_id,
                    'herf': f"/v1/query/chunk?id={chunk_id}"
                }
            ]
        }

    def post(self):
        resource = {
            'id' : chunk_id,
            'herf': f"/v1/query/chunk?id={chunk_id}", 
            
        }
        return resource

@API.route("/v1/query/chunk")
class V1QueryChunk(Resource):
    def get(self):
        id = request.args.get('id')
        if id != chunk_id:
            return {}
        some_args = []
        return {
            'id' : chunk_id,
            'center' : [-3500, -3500, 0],
            'min-bound' : [-5000, -5000, -1000],
            'max-bound' : [-3000, -3000, 1000],
            'last-update' : "2023-04-04 12:00:00",
            'geo-origin' : [-33.5, 151.5],
            'parent': 's34_e151_1arc_v3.tif',
            'status' : {
                'Mesh' : {
                    "exist" : True,
                    'id' : mesh_resource_id,
                    'herf': f"/v1/resource?id={mesh_resource_id}", 
                    'download' : f"/v1/download/{mesh_resource_id}",
                    'expired' : 3
                },
                'Pcd' : {
                    "exist" : False,
                    'herf' : f"/v1/resource",
                    'args' : some_args
                },
            },
        }


@API.route("/v1/resource")
class V1Resource(Resource):
    def get(self):
        id = request.args.get("id")
        print(id)
        if id == mesh_resource_id:
            file = open("data/meshs/chunk.ply", "rb")
            return Response(file.read(), mimetype="application/octet-stream")
        pass

    def post(self):
        data = json.loads(request.get_json())
        def do_some_stuff(data):
            pass
        do_some_stuff(data)
        time.sleep(2)

        return {
            'id' : pcd_resource_id,
            'herf': f"/v1/resource?id={pcd_resource_id}",
            'expired' : 3
        }  

@API.route("/v1/download/<string:id>")
class V1Download(Resource):
    def get(self, id):
        # url = request.args.get("id")

        # id = "data/meshs/chunk.ply"
        if id == mesh_resource_id:
            pth = "data/meshs/chunk.ply"
        else:
            return {}
        CHUNK_SIZE = 4096
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
                stream_with_context(read_file_chunks(pth)),
                headers={
                    'Content-Disposition': f'attachment; filename={"test_download.ply"}'
                }
            )
        except FileNotFoundError:
            return {"message" : "invalid id"}















# @API.route("/query/mesh", methods=['POST'])
# def get_meshs():
#     data = request.get_json()
#     assert type(data['polygon']) is list
#     ids = Manager().searchChunk(data['polygon'])
#     urls = []
#     for id in ids:
#         url = Manager().getChunkSavedURL(id, ".ply")
#         if url is None:
#             continue
#         urls.append(url)
#     return json.dumps(urls)

# @API.route("/temp/ln", methods=['POST'])
# def make_link():
#     src = os.path.abspath("data/meshs")
#     pths = request.get_json()
#     for pth in pths['path']:
#         os.symlink(src, pth)
#     return {}

# @API.route("/download/mesh", methods=['GET'])
# def get_download():
#     url = request.args.get("pth")
#     CHUNK_SIZE = 8192
#     def read_file_chunks(url):
#         with open(url, 'rb') as fd:
#             while 1:
#                 buf = fd.read(CHUNK_SIZE)
#                 if buf:
#                     yield buf
#                 else:
#                     break
#     try:
#         return Response(
#             stream_with_context(read_file_chunks(url)),
#             headers={
#                 'Content-Disposition': f'attachment; filename={"123.ply"}'
#             }
#         )
#     except FileNotFoundError:
#         return {"message" : "invalid id"}


if __name__ == "__main__":
    # signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    # Manager().load()
    app.run(port=PORT) # Do not edit this port