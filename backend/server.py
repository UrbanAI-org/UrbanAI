from flask import Flask, request, make_response, Response, stream_with_context
# from flask_cors import CORS
from flask_restx import Api, Resource, fields, inputs, reqparse
# from flask_restx import 
import json
import traceback
import os
import time
from src.database.database import database
from src.loaders.tifLoader import Loader
# from src.resources.resource import load_from_meshes, load_from_pcds, process_pcd, process_mesh
from src.fetchers.ResourceFetcher import ResourceFetcher
from src.fetchers.RegionDataFetcher import RegionDataFetcher
from src.fetchers.Fetchersconsts import ResourceType
PORT = 9999


app = Flask(__name__)
API = Api(app)
# APP.config['TRAP_HTTP_EXCEPTIONS'] = True
# APP.register_error_handler(Exception, defaultHandler)
# chunk_id = "153370ea-07a4-4f96-a0d7-d7650111ab66"
# chunk_id = "abc"
# mesh_resource_id = "4aa5660c-bff0-472d-bc66-0868a1477acf"
# mesh_resource_id = "4aa5660c-bff0-472d-bc66-0868a1477acf"
# pcd_resource_id = "b16be8bf-4c0d-4898-9a63-f683f9f2cb7a"
# pcd_resource_id = "b16be8bf-4c0d-4898-9a63-f683f9f2cb7a"

# @API.route("/v1/query/chunks")
# class V1QueryChunks(Resource):
#     def get(self):
        
#         return {
#             }

#     def post(self):
#         data = request.json
#         tif = database.execute_in_worker("select uid, origin_lat, origin_lon from tifs where filename=?", ['s34_e151_1arc_v3.tif'])[0]
#         if data['type'] == 'polygon':
#             chunk = RegionDataFetcher.create_by_polygon(data['data']['polygon'], tif[1:], tif[0])
#         elif data['type'] == 'circle':
#             chunk = RegionDataFetcher.create_by_circle(data['data']['center'], data['data']['radius'], tif[1:], tif[0])
#         else:
#             return {"message" : "invalid input"}, 400
#         chunk.write_to_database()
#         resource = {
#             'id' : chunk.id,
#             'herf': f"/v1/query/chunk?id={chunk.id}", 
#         }
#         return resource

# @API.route("/v1/query/chunk")
# class V1QueryChunk(Resource):
#     def get(self):
#         id = request.args.get('id')
#         chunk = RegionDataFetcher.read_from_database(id)
#         if chunk is None:
#             return {}
#         return chunk.to_response()

# @API.route("/v1/resource")
# class V1Resource(Resource):
#     def get(self):
#         id = request.args.get("id")
#         print(id)
#         resource_type = request.args.get("type", "mesh")
#         if resource_type == "mesh":
#             path = load_from_meshes(id)
#         elif resource_type == "pcb":
#             path = load_from_pcds(id)
#         else:
#             return {"message" : "invalid format"}, 400
#         if path is None:
#             return {"message" : "invalid id"}, 400
#         else:
#             file = open(path, "rb")
#             file_str = base64.b64encode(file.read())
#             file.close()
#             return Response(file_str, mimetype="text/plain")
        

#     def post(self):
#         data = request.get_json()
#         chunk = RegionDataFetcher.read_from_database(data['chunk_id'])
#         if chunk is None:
#             return {"message" : "chunk does not exist"}, 404
#         if data['type'] == 'mesh':
#             process_mesh(chunk)
#         elif data['type'] == 'pcd':
#             process_pcd(chunk)
#         else:
#             return {"message" : "invalid type"}, 400
#         return {
#             'id' : chunk,
#             'herf': f"/v1/resource?id={chunk}&type={data['type']}",
#             'expired' : 3
#         }  

@API.route("/v1/download")
class V1Download(Resource):
    def get(self):
        resource_type = request.args.get("type", "mesh")
        id = request.args.get("id", None)
        if resource_type == "mesh":
            path = ResourceFetcher.load_from_meshes(id)
        elif resource_type == "pcb":
            path = ResourceFetcher.load_from_pcds(id)
        else:
            return {"message" : "invalid format"}
        if path is None:
            return {"message" : "invalid id"}, 400
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
                stream_with_context(read_file_chunks(path)),
                headers={
                    'Content-Disposition': f'attachment; filename={"test_download.ply"}'
                }
            )
        except FileNotFoundError:
            return {"message" : "invalid id"}, 400


def phrase_polygon(data):
    polygon = []
    for each in data:
        polygon.append(phrase_lat_lon(each))
    return polygon

def phrase_lat_lon(data):
    return [data['latitude'], data['longitude']]

@API.route("/v1/api/region/mesh")
class V1ApiRegionAdd(Resource):
    def post(self):
        data = request.json
        tif = database.execute_in_worker("select uid, origin_lat, origin_lon from tifs where filename=?", ['s34_e151_1arc_v3.tif'])[0]
        if data['type'] == 'polygon':
            chunk = RegionDataFetcher.create_by_polygon(phrase_polygon(data['data']), tif[1:], tif[0])
        elif data['type'] == 'circle':
            chunk = RegionDataFetcher.create_by_circle(phrase_lat_lon(data['data']['center']), data['data']['radius'], tif[1:], tif[0])
        else:
            return {"message" : "invalid input"}, 400
        chunk.make_mesh()
        chunk.write_to_database()
        downlink = chunk.make_link(ResourceType.MESH)
        mesh = chunk.get_mesh()
        return {
            "download" : downlink,
            "mesh" : mesh,
            "details" : chunk.to_details()
        }









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
    database.start()
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunk = loader.toChunkWithXYPlaneCoord()
    chunk.toPointCloud(save=True)
    chunk.toMesh(save=True)
    app.run(port=PORT) 