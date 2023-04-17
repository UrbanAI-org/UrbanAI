from src.database.database import database
from geopy import distance
import uuid
import open3d as o3d
import numpy as np
from datetime import datetime

def _relativeDistance(given : tuple, base: tuple) -> float:
    """
    return relative distance based on two points.
    """
    distance_ = distance.distance(given, base).m
    if given[0] < base[0] or given[1] < base[1]:
        return -1 * distance_
    return distance_

def string_to_radius(string):
    if type(string) is not str:
        return string * 1000
    option = {
        "km" : 1000,
        "m" : 1,
        "yard" : 0.9144,
        "mile" : 1609.344,
    }
    distance = int(''.join(filter(str.isdigit, string)))
    unit = str(''.join(filter(str.isalpha, string))).lower()
    if unit not in option.keys():
        return distance
    return distance * option[unit]



class RegionDataFetcher:
    def __init__(self, center, min_bound, max_bound,base, parent, id = None) -> None:
        pass
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.center = center
        self.min = min_bound
        self.max = max_bound
        self.base = base
        self.parent = parent
        self.mesh = None
        self.pcd = None
        self.max_altitude  = None
        self.min_altitude  = None

    @staticmethod
    def create_by_polygon(polygon, base, parent):
        polygon = [RegionDataFetcher.to_XY_Plane(each, base) for each in polygon]
        lats = [row[0] for row in polygon]
        lons = [row[1] for row in polygon]
        min_bound = [min(lats), min(lons)]
        max_bound = [max(lats), max(lons)]
        center = [sum(lats) / len(lats), sum(lons) / len(lons)]
        return RegionDataFetcher(center, min_bound, max_bound, base, parent)

    @staticmethod
    def create_by_circle(center, radius, base, parent):
        center = RegionDataFetcher.to_XY_Plane(center, base)
        radius = string_to_radius(radius)
        lats = [center[0] + radius, center[0] - radius]
        lons = [center[1] + radius, center[1] - radius]
        min_bound = [min(lats), min(lons)]
        max_bound = [max(lats), max(lons)]
        return RegionDataFetcher(center, min_bound, max_bound, base, parent)

    @staticmethod
    def to_XY_Plane(coord, base):
        xy = [
            _relativeDistance((coord[0], base[1]), base),
            _relativeDistance((base[0], coord[1]), base),
        ]
        return xy

    def write_to_database(self):
        qry = f"""
        insert or replace into chunks(id, center_x, center_y, min_bound_x, min_bound_y, max_bound_x, max_bound_y, origin_lat, origin_lon, parent, pcd, mesh, max_altitude, min_altitude)
        values ({','.join(['?'] * 14)});
        """
        param = [
            self.id, self.center[0], self.center[1], self.min[0], self.min[1], self.max[0], self.max[1], self.base[0], self.base[1], self.parent, self.pcd, self.mesh, self.max_altitude, self.min_altitude
        ]
        print(param)
        database.execute_in_worker(qry, param)
        pass
    @staticmethod
    def read_from_database(id):
        """
        TODO: load region from database. not sure whether this still useful.
        """
        pass
        return None
        qry = """
        select * from chunks where id = ?;
        """
        data = database.execute_in_worker(qry, [id])
        if len(data) == 0:
            return None
        data = data[0]
        index = {
            "id" :  0,
            "center_x" : 1 ,
            "center_y" :  2,
            "min_bound_x" :  3,
            "min_bound_y" :  4,
            "max_bound_x" :  5,
            "max_bound_y" :  6,
            "origin_lat" :  7,
            "origin_lon" :  8,
            "parent" :  9,
            "pcd"  :  10,
            "mesh" : 11,
        }
        chunk = RegionDataFetcher([data[index['center_x']], data[index["center_y"]]],
                      [data[index["min_bound_x"]], data[index["min_bound_y"]]],
                      [data[index['max_bound_x']], data[index["max_bound_y"]]],
                      [data[index['origin_lat']], data[index["origin_lon"]]],
                      data[index['parent']], data[index['id']]
                      )
        # if data[index["pcd"]] is not None:
        #     qry = """
        #     select uid, expired from pcds where id = ?;
        #     """
        #     pcd = database.execute_in_worker(qry, [data[index["pcd"]]])[0]
        #     chunk.pcd = {
        #         'id' : pcd[0],
        #         'expired' : pcd[1]
        #     }
        # if data[index['mesh']] is not None:
        #     qry = """
        #     select uid,expired from meshes where id = ?;
        #     """
        #     mesh = database.execute_in_worker(qry, [data[index["mesh"]]])[0]
        #     chunk.mesh = {
        #         'id' : mesh[0],
        #         'expired' : mesh[1]
        #     }
        return chunk
        # database.execute_in_worker()

    def to_response(self):
        qry = """
        select filename from tifs where uid = ?;"""
        filename = database.execute_in_worker(qry, [self.parent])[0][0]
        response = {
            'id' : self.id,
            'center' : self.center + [0],
            'min-bound' : self.min + [-1000],
            'max-bound' : self.max + [3000],
            'geo-origin' : self.base,
            'parent': filename,
            'status' : { 'Mesh' : self._make_file_response(self.mesh, 'mesh'),
                        'Pcd' : self._make_file_response(self.pcd, 'pcd') },
        }
        return response

    def _make_file_response(self, file, file_type):
        response = {}
        exist = file is not None
        response.update({ "exist" : exist})
        response.update(self._make_resource_url(file, file_type, exist))
        response.update(self._make_download_url(file, file_type, exist))
        if exist:
            response.update(file)
        return response

    def _make_resource_url(self, file, file_type, exist=True):
        if exist:
            return {
                'herf': f"/v1/resource?id={file['id']}&type={file_type}",
            }
        else:
            return {
                'herf': f"/v1/resource",
                'args' : {
                    "chunk_id" : self.id,
                    "type" : file_type
                }

            }

    def _make_download_url(self, file, file_type, exist=True):
        if not exist:
            return {}
        else:
            return {
                'download' : f"/v1/download?id={file['id']}&type={file_type}",
            }

    def to_bbox(self):
        bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [-1000]), np.array(self.max + [3000]))
        return bbox

    def make_mesh(self):
        qry = """
        select pth from meshes where uid = ?;
        """
        data = database.execute_in_worker(qry, [self.parent])[0]
        mesh = o3d.io.read_triangle_mesh(data[0])
        croped_mesh = mesh.crop(self.to_bbox())
        if len(croped_mesh.triangles) == 0:
            return
        mesh_id = str(uuid.uuid4())
        o3d.io.write_triangle_mesh(f"data/meshes/{mesh_id}.ply", croped_mesh, print_progress = True)
        qry = """
            insert or replace into meshes(uid, expired, last_update, pth)
            values (?,?,?,?);
            """
        database.execute_in_worker(qry, [mesh_id, 3, datetime.now().timestamp(), f"data/meshes/{mesh_id}.ply"])
        qry = """
            select id from meshes where uid = ?;
        """
        id = database.fetchone(qry, [mesh_id])
        self.mesh = id[0]
        self.max_altitude = croped_mesh.get_max_bound().tolist()[2]
        self.min_altitude = croped_mesh.get_min_bound().tolist()[2]
        pass

    def make_pointcloud(self):
        qry = """
        select pth from pcds where uid = ?;
        """
        data = database.execute_in_worker(qry, [self.parent])[0]
        pcd = o3d.io.read_point_cloud(data[0])
        croped_pcd = pcd.crop(self.to_bbox())
        pcd_id = str(uuid.uuid4())
        o3d.io.write_point_cloud(f"data/pcds/{pcd_id}.pcd", croped_pcd, print_progress = True)
        qry = """
            insert or replace into pcds(uid, expired, last_update, pth)
            values (?,?,?,?);
            """
        database.execute_in_worker(qry, [pcd_id, 3, datetime.now().timestamp(), f"data/pcds/{pcd_id}.pcd"])
        qry = """
            select id from pcds where uid = ?;
        """
        id = database.fetchone(qry, [pcd_id])
        self.pcd = id[0]
        self.max_altitude = croped_pcd.get_max_bound().tolist()[2]
        self.min_altitude = croped_pcd.get_min_bound().tolist()[2]

    def to_details(self):
        return {
            'id' : self.id,
            'center' : self.center + [(self.max_altitude + self.min_altitude) / 2],
            'min-bound' : self.min + [self.min_altitude],
            'max-bound' : self.max + [self.max_altitude],
            'geo-origin' : self.base,
        }

    def make_link(self, type):
        if type == "mesh":
            qry = """
            select uid from meshes where id = ?;
            """
            uid = database.fetchone(qry, [self.mesh])[0]
            return f"/v1/download?id={uid}&type=mesh"