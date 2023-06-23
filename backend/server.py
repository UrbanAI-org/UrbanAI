from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource
# from flask_restx import
import json
from src.database.database import database
from src.loaders.TifLoader import TifLoader
# from src.resources.resource import load_from_meshes, load_from_pcds, process_pcd, process_mesh
from src.fetchers.ResourceFetcher import MeshResourceFetcher, PcdResourceFetcher
from src.fetchers.RegionDataFetcher import RegionDataFetcher
from src.fetchers.FetchersConsts import ResourceType, ResourceAttr
from src.fetchers.TifRegionFetcher import TifRegionFetcher
from src.fetchers.TifFetcher import TifFetcher
import time
from src.always_on.CacheClear import CaCheClear, RegionsClear
from src.always_on.AlwaysOnLauncher import Launcher
from datetime import timedelta
from src.exceptions.ServerExceptions import InvalidResourceId, InvalidRequestType, InvalidInput, LargeSelectedArea, InvalidAuth, ResourceNotFound
CLEAR_CACHE = hash(time.time())

PORT = 9999
app = Flask(__name__)

CORS(app, origins="*")



# app.config['TRAP_HTTP_EXCEPTIONS'] = True
# app.register_error_handler(Exception, defaultHandler)
API = Api(app)

@API.route("/v1/map/key")
class MapKey(Resource):
    def post(self):
        pass

@API.route("/v1/clear/cache")
class ClearCache(Resource):
    def delete(self):
        data = request.json
        if data['key'] == CLEAR_CACHE:
            database.clear_cache()
            database.report()
            # raise
            return {"message" : "Successed"}, 200
        else:
            raise InvalidAuth("You have no premission.")
        
@API.route("/v1/clear/regions")
class ClearRegions(Resource):
    def delete(self):
        data = request.json
        if data['key'] == CLEAR_CACHE:
            database.clear_regions()
            database.report()
            return {"message" : "Successed"}, 200
        else:
            raise InvalidAuth("You have no premission.")


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
            raise InvalidRequestType(f"Invalid format {resource_type}, expect mesh or pcb.")
        if path is None:
            raise InvalidResourceId(f"Invalid Resource ID {id}, please check the url agagin")
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
            raise ResourceNotFound("Resource not found.")


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
        try:
            if data['type'] == 'polygon':
                chunk = RegionDataFetcher.create_by_polygon(phrase_polygon(data['data']))
            elif data['type'] == 'circle':
                chunk = RegionDataFetcher.create_by_circle(phrase_lat_lon(data['data']), data['data']['radius'])
            else:
                raise InvalidRequestType(f"Invalid format {data['type']}, expect polygon or circle.")
        except KeyError:
            raise InvalidRequestType("You must include a type with data.")
        if database.in_cache(chunk.to_range_string()):
            print("requested area is in cache")
            data = database.get_cache(chunk.to_range_string())
            chunk = RegionDataFetcher.read_from_database(data['id'])
            downlink = data['download_link']
        else:
            chunk.make_mesh()
            chunk.write_to_database()
            downlink = chunk.make_link(ResourceType.MESH)
            database.put_cache(chunk.to_range_string(), {"id" : chunk.id, "download_link": downlink, "mesh_id": chunk.mesh})
        return {
            "download" : downlink,
            "details" : chunk.to_details()
        }
    def options(self):

        return Response(headers={"Access-Control-Allow-Methods" : "POST,GET,DELETE,OPTIONS"})

@API.errorhandler
def defaultHandler(err):
    # response = err.get_response()
    print('response', err)
    response = {
        "name": "System Error",
        "message": str(err),
    }

    return response, getattr(err, 'code', 500)

if __name__ == "__main__":
    database.start()
    database.report()
    # print("Open file:", "s34_e151_1arc_v3.tif")
    # loader = TifLoader("data/s34_e151_1arc_v3.tif", origin=[(-35 + -30) / 2, (148+150) / 2])
    # fetcher = TifRegionFetcher.create_by_loader(loader)
    # fetcher.make_pcd()
    # fetcher.make_mesh()
    
    launch = Launcher()
    launch.add(CaCheClear(CLEAR_CACHE, timedelta(hours=3)))
    launch.add(RegionsClear(CLEAR_CACHE, timedelta(hours=6)))
    launch.launch()
    print("Sensitive Operation Hash Key:", CLEAR_CACHE)
    app.run(port=PORT)