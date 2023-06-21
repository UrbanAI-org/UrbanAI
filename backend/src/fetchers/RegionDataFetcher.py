import base64
from src.database.database import database
from geopy import distance
import uuid
import open3d as o3d
import numpy as np 
from datetime import datetime
import src.fetchers.ResourceFetcher as ResourceFetcher
from src.fetchers.FetchersConsts import ResourceType, ResourceAttr
from src.fetchers.TifFetcher import TifFetcher
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
        return distance * 1000
    return distance * option[unit]



class RegionDataFetcher:
    def __init__(self, center, min_bound, max_bound,base, parents, max_altitude = -1000, min_altitude=10000, mesh = None, pcd = None, id = None) -> None:
        pass
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.center = center
        self.min = min_bound
        self.max = max_bound
        self.base = base
        self.parents = parents
        self.mesh = None 
        self.pcd = None
        self.max_altitude  = max_altitude 
        self.min_altitude  = min_altitude    

    @staticmethod
    def create_by_polygon(polygon):
        base, parents = TifFetcher.fetch_by_polygon(polygon)
        polygon = [RegionDataFetcher.to_XY_Plane(each, base) for each in polygon]
        lats = [row[0] for row in polygon]
        lons = [row[1] for row in polygon]
        min_bound = [min(lats), min(lons)]
        max_bound = [max(lats), max(lons)]
        center = [sum(lats) / len(lats), sum(lons) / len(lons)]
        return RegionDataFetcher(center, min_bound, max_bound, base, parents)

    @staticmethod
    def create_by_circle(center, radius):
        radius = string_to_radius(radius)
        base, parents = TifFetcher.fetch_by_circle(center, radius)
        center = RegionDataFetcher.to_XY_Plane(center, base)
        lats = [center[0] + radius, center[0] - radius]
        lons = [center[1] + radius, center[1] - radius]
        min_bound = [min(lats), min(lons)]
        max_bound = [max(lats), max(lons)]
        return RegionDataFetcher(center, min_bound, max_bound, base, parents)

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
            self.id, self.center[0], self.center[1], self.min[0], self.min[1], self.max[0], self.max[1], self.base[0], self.base[1], ",".join(self.parents), self.pcd, self.mesh, self.max_altitude, self.min_altitude
        ]
        print(param)
        database.execute_in_worker(qry, param)

    @staticmethod
    def read_from_database(id):
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
            "parents" :  9,
            "pcd"  :  10,
            "mesh" : 11,
            "max_altitude" : 12,
            "min_altitude" : 13,
        }
        region = RegionDataFetcher([data[index['center_x']], data[index["center_y"]]], 
                      [data[index["min_bound_x"]], data[index["min_bound_y"]]],
                      [data[index['max_bound_x']], data[index["max_bound_y"]]],
                      [data[index['origin_lat']], data[index["origin_lon"]]],
                      data[index['parents']].split(","), data[index['max_altitude']], data[index['min_altitude']],
                      mesh=data[index['mesh']], pcd=data[index['pcd']],
                      id = data[index['id']]
                      )
        return region
    
        
    def get_bbox(self):
        bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [self.min_altitude]), np.array(self.max + [self.max_altitude]))
        return bbox
    
    def get_mesh(self, encoded = lambda data: base64.b64encode(data).decode("utf-8")):
        fetcher = ResourceFetcher.MeshResourceFetcher()
        file = fetcher.get_content(ResourceFetcher.ResourceAttr.DB_ID, self.mesh)
        binary_file_data = file.read()
        return encoded(binary_file_data)

    def get_pcd(self, encoded = lambda data: base64.b64encode(data).decode("utf-8")):
        fetcher = ResourceFetcher.PcdResourceFetcher()
        file = fetcher.get_content(ResourceFetcher.ResourceAttr.DB_ID, self.pcd)
        binary_file_data = file.read()
        return  encoded(binary_file_data)

    def make_mesh(self, save=True):
        fetcher = ResourceFetcher.MeshResourceFetcher()
        path = fetcher.get_pth(ResourceFetcher.ResourceAttr.UNIQUE_ID, self.parents)
        if len(path) == 1:
            mesh = o3d.io.read_triangle_mesh(path[0])
            bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [-1000]), np.array(self.max + [10000]))
            croped_mesh = mesh.crop(bbox)
        else:
            pcd = self.make_pointcloud(save=False)
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd)
            bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd.points)
            croped_mesh = mesh.crop(bbox)
        if len(croped_mesh.triangles) == 0:
            print("bbox too small")
            return None
        if save:
            mesh_id = str(uuid.uuid4())
            path = f"data/meshes/{mesh_id}.ply"
            o3d.io.write_triangle_mesh(path, croped_mesh, print_progress = True)
            self.mesh = fetcher.write_to_database(mesh_id, path)
        self.max_altitude = croped_mesh.get_max_bound().tolist()[2]
        self.min_altitude = croped_mesh.get_min_bound().tolist()[2]
        return croped_mesh

    def make_pointcloud(self, save=True):
        fetcher = ResourceFetcher.PcdResourceFetcher()
        paths = fetcher.get_pth(ResourceFetcher.ResourceAttr.UNIQUE_ID, self.parents)
        pcd = o3d.geometry.PointCloud()
        for path in paths:
            pcd += o3d.io.read_point_cloud(path)
        bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [-1000]), np.array(self.max + [10000]))
        croped_pcd = pcd.crop(bbox)
        if save:
            pcd_id = str(uuid.uuid4())
            path = f"data/pcds/{pcd_id}.pcd"
            o3d.io.write_point_cloud(path, croped_pcd, print_progress = True)
            self.pcd = fetcher.write_to_database(pcd_id, path)
        self.max_altitude = croped_pcd.get_max_bound().tolist()[2]
        self.min_altitude = croped_pcd.get_min_bound().tolist()[2]
        return croped_pcd

    def to_details(self):
        return {
            'id' : self.id,
            'center' : self.center + [(self.max_altitude + self.min_altitude) / 2],
            'min-bound' : self.min + [self.min_altitude],
            'max-bound' : self.max + [self.max_altitude],
            'geo-origin' : self.base,
        }
    
    def make_link(self, resource_type):
        assert type(resource_type) is ResourceType
        if resource_type == ResourceType.MESH:
            fetcher = ResourceFetcher.MeshResourceFetcher()
            uid = fetcher.get_uid(ResourceAttr.DB_ID, self.mesh)
        else:
            fetcher = ResourceFetcher.PcdResourceFetcher()
            uid = fetcher.get_uid(ResourceAttr.DB_ID, self.pcd)
        if uid is None:
            raise ValueError("uid does not exist")
        
        return f"/v1/download?id={uid}&type=mesh"

    def to_range_string(self):
        return f"{self.min}-{self.max}"