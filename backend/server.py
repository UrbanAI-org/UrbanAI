from flask import Flask, request, make_response, Response, stream_with_context
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource, fields, inputs, reqparse
# from flask_restx import
import json
import traceback
import os
import time
from src.database.database import database
from src.loaders.TifLoader import TifLoader
# from src.resources.resource import load_from_meshes, load_from_pcds, process_pcd, process_mesh
from src.fetchers.ResourceFetcher import MeshResourceFetcher, PcdResourceFetcher
from src.fetchers.RegionDataFetcher import RegionDataFetcher
from src.fetchers.FetchersConsts import ResourceType, ResourceAttr
from src.fetchers.TifRegionFetcher import TifRegionFetcher
PORT = 9999
app = Flask(__name__)

CORS(app, origins="*")


API = Api(app)

@API.route("/v1/download")
class V1Download(Resource):
    def get(self):
        resource_type = request.args.get("type", "mesh")
        id = request.args.get("id", None)
        if resource_type == "mesh":
            fetcher = MeshResourceFetcher()
            path = fetcher.get_pth(ResourceAttr.UNIQUE_ID, id)
        elif resource_type == "pcb":
            fetcher = PcdResourceFetcher()
            path = fetcher.get_pth(ResourceAttr.UNIQUE_ID, id)
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
    return [float(data['latitude']), float(data['longitude'])]

@cross_origin
@API.route("/v1/api/region/mesh")
class V1ApiRegionAdd(Resource):
    def post(self):
        if request.headers.get("Content-Type") == "text/plain":
            data = json.loads(request.data)
        else:
            data = request.json
        print(data)
        tif = database.execute_in_worker("select uid, origin_lat, origin_lon from tifs where filename=?", ['s34_e151_1arc_v3.tif'])[0]
        if data['type'] == 'polygon':
            chunk = RegionDataFetcher.create_by_polygon(phrase_polygon(data['data']), tif[1:], tif[0])
        elif data['type'] == 'circle':
            chunk = RegionDataFetcher.create_by_circle(phrase_lat_lon(data['data']), data['data']['radius'], tif[1:], tif[0])
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
    def options(self):

        return Response(headers={"Access-Control-Allow-Methods" : "POST,GET,DELETE,OPTIONS"})









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
    loader = TifLoader("data/s34_e151_1arc_v3.tif")
    fetcher = TifRegionFetcher.create_by_loader(loader)
    fetcher.make_pcd()
    fetcher.make_mesh()
    app.run(port=PORT)