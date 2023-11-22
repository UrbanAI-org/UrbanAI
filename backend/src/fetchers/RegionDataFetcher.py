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
from src.fetchers.Exceptions import BBoxIsSmall, BBoxIsLarge
def _relativeDistance(given : tuple, base: tuple) -> float:
    """
    Return the relative distance between two points.

    Parameters:
    given (tuple): The coordinates of the given point.
    base (tuple): The coordinates of the base point.

    Returns:
    float: The relative distance between the given point and the base point.
    """
    distance_ = distance.distance(given, base).m 
    if given[0] < base[0] or given[1] < base[1]:
        return -1 * distance_
    return distance_

def string_to_radius(string):
    """
    Converts a string representation of distance to radius in meters.

    Args:
        string (str): The string representation of distance. Example: "10km", "5miles", "1000m".

    Returns:
        int: The radius in meters.

    Raises:
        None

    """
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
    def __init__(self, center, min_bound, max_bound, base, parents, max_altitude=-1000, min_altitude=10000, mesh=None, pcd=None, id=None) -> None:
            """
            Initialize a RegionDataFetcher object.

            Args:
                center (tuple): The center coordinates of the region.
                min_bound (tuple): The minimum boundary coordinates of the region.
                max_bound (tuple): The maximum boundary coordinates of the region.
                base (str): The base of the region.
                parents (list): The list of parent regions.
                max_altitude (float, optional): The maximum altitude of the region. Defaults to -1000.
                min_altitude (float, optional): The minimum altitude of the region. Defaults to 10000.
                mesh (object, optional): The mesh object of the region. Defaults to None.
                pcd (object, optional): The point cloud data of the region. Defaults to None.
                id (str, optional): The ID of the region. If not provided, a new ID will be generated.

            Raises:
                BBoxIsLarge: If the given region is too large to process.
            """
            pass
            if id is None:
                self.id = str(uuid.uuid4())
            else:
                self.id = id
            self.center = center
            if ((np.array(max_bound) - np.array(min_bound)) > 11_000).sum() > 0:
                raise BBoxIsLarge("Given region is too large to process")
            self.min = min_bound
            self.max = max_bound
            self.base = base
            self.parents = parents
            self.mesh = None 
            self.pcd = None
            self.max_altitude = max_altitude 
            self.min_altitude = min_altitude

    @staticmethod
    def create_by_polygon(polygon):
        """
        Create a RegionDataFetcher object based on a given polygon.

        Args:
            polygon (list): List of coordinates representing the polygon.

        Returns:
            RegionDataFetcher: The created RegionDataFetcher object.
        """
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
        """
        Create a RegionDataFetcher object based on a given center and radius.

        Args:
            center (tuple): The center coordinates of the circle.
            radius (float): The radius of the circle.

        Returns:
            RegionDataFetcher: The created RegionDataFetcher object.
        """
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
        """
        Converts the given coordinate to the XY plane based on the given base coordinate.

        Args:
            coord (tuple): The coordinate to be converted.
            base (tuple): The base coordinate.

        Returns:
            list: The converted coordinate in the XY plane.
        """
        xy = [
            _relativeDistance((coord[0], base[1]), base),
            _relativeDistance((base[0], coord[1]), base),
        ]
        return xy
    
    def write_to_database(self):
        """
        Writes the region data to the database.

        This method inserts or replaces a record in the 'chunks' table of the database
        with the region data provided.

        Args:
            None

        Returns:
            None
        """
        qry = f"""
        insert or replace into chunks(id, center_x, center_y, min_bound_x, min_bound_y, max_bound_x, max_bound_y, origin_lat, origin_lon, parent, pcd, mesh, max_altitude, min_altitude) 
        values ({','.join(['?'] * 14)});
        """
        param = [
            self.id, self.center[0], self.center[1], self.min[0], self.min[1], self.max[0], self.max[1], self.base[0], self.base[1], ",".join(self.parents), self.pcd, self.mesh, self.max_altitude, self.min_altitude
        ]
        database.execute_in_worker(qry, param)

    @staticmethod
    def read_from_database(id):
        """
        Reads region data from the database based on the given ID.

        Args:
            id (int): The ID of the region to fetch.

        Returns:
            RegionDataFetcher: An instance of the RegionDataFetcher class representing the fetched region data.
                Returns None if no data is found for the given ID.
        """
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
        """
        Get the bounding box of the region.

        Returns:
            o3d.geometry.AxisAlignedBoundingBox: The bounding box of the region.
        """
        bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [self.min_altitude]), np.array(self.max + [self.max_altitude]))
        return bbox
    
    def get_mesh(self, encoded = lambda data: base64.b64encode(data).decode("utf-8")):
        """
        Fetches the mesh data and returns it as an encoded string.

        Parameters:
        - encoded (function): A function that encodes the binary file data. Default is base64 encoding.

        Returns:
        - str: The encoded mesh data.
        """
        fetcher = ResourceFetcher.MeshResourceFetcher()
        file = fetcher.get_content(ResourceFetcher.ResourceAttr.DB_ID, self.mesh)
        binary_file_data = file.read()
        return encoded(binary_file_data)

    def get_pcd(self, encoded = lambda data: base64.b64encode(data).decode("utf-8")):
        """
        Fetches the PCD file associated with the region and returns it as an encoded string.

        Parameters:
        - encoded (function): A function that encodes the file data. Default is base64 encoding.

        Returns:
        - str: The encoded PCD file data.
        """
        fetcher = ResourceFetcher.PcdResourceFetcher()
        file = fetcher.get_content(ResourceFetcher.ResourceAttr.DB_ID, self.pcd)
        binary_file_data = file.read()
        return  encoded(binary_file_data)

    
    def make_mesh(self, save=True):
        """
        Generates a mesh for the region.

        Args:
            save (bool, optional): Whether to save the generated mesh. Defaults to True.

        Returns:
            o3d.geometry.TriangleMesh: The generated mesh.
        """
        fetcher = ResourceFetcher.MeshResourceFetcher()
        path = fetcher.get_pth(ResourceFetcher.ResourceAttr.UNIQUE_ID, self.parents)
        # print(path)
        if len(path) == 1:
            print("Within a path", path)
            mesh = o3d.io.read_triangle_mesh(path[0])
            bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [-1000]), np.array(self.max + [10000]))
            croped_mesh = mesh.crop(bbox)
        else:
            print("Generating Mesh required ...")
            print("load pcds")
            pcd = self.make_pointcloud(save=False, pcd_scale=1.2)
            print("make")
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth = 6)
            bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [-1000]), np.array(self.max + [10000]))
            croped_mesh = mesh.crop(bbox)
        if len(croped_mesh.triangles) == 0:
            raise BBoxIsSmall("Given area is small. None of the triangule meshes exist.")
        if save:
            mesh_id = str(uuid.uuid4())
            path = f"data/meshes/{mesh_id}.ply"
            o3d.io.write_triangle_mesh(path, croped_mesh, print_progress = True)
            self.mesh = fetcher.write_to_database(mesh_id, path)
        self.max_altitude = croped_mesh.get_max_bound().tolist()[2]
        self.min_altitude = croped_mesh.get_min_bound().tolist()[2]
        return croped_mesh

    def make_pointcloud(self, save=True, pcd_scale=1):
        """
        Generates a point cloud by reading multiple point cloud files, cropping them based on a bounding box,
        removing duplicated points, estimating normals, and optionally saving the resulting point cloud.

        Args:
            save (bool, optional): Whether to save the resulting point cloud. Defaults to True.
            pcd_scale (float, optional): Scaling factor for the bounding box. Defaults to 1.

        Returns:
            o3d.geometry.PointCloud: The resulting cropped and processed point cloud.
        """
        fetcher = ResourceFetcher.PcdResourceFetcher()
        paths = fetcher.get_pth(ResourceFetcher.ResourceAttr.UNIQUE_ID, self.parents)
        pcd = o3d.geometry.PointCloud()
        bbox = o3d.geometry.AxisAlignedBoundingBox(np.array(self.min + [-1000]), np.array(self.max + [10000]))
        bbox.scale(pcd_scale, bbox.get_center())
        for path in paths:
            pcd += o3d.io.read_point_cloud(path).crop(bbox)
        croped_pcd = pcd.remove_duplicated_points()
        croped_pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
        croped_pcd.estimate_normals()
        if save:
            pcd_id = str(uuid.uuid4())
            path = f"data/pcds/{pcd_id}.pcd"
            print(path)
            o3d.io.write_point_cloud(path, croped_pcd, print_progress=True)
            self.pcd = fetcher.write_to_database(pcd_id, path)
        self.max_altitude = croped_pcd.get_max_bound().tolist()[2]
        self.min_altitude = croped_pcd.get_min_bound().tolist()[2]
        return croped_pcd

    def to_details(self):
        """
        Convert the RegionDataFetcher object to a dictionary containing details.

        Returns:
            dict: A dictionary containing the details of the RegionDataFetcher object.
                    The dictionary includes the following keys:
                    - 'id': The ID of the object.
                    - 'center': The center coordinates of the object, including the average altitude.
                    - 'min-bound': The minimum coordinates of the object, including the minimum altitude.
                    - 'max-bound': The maximum coordinates of the object, including the maximum altitude.
                    - 'geo-origin': The base coordinates of the object.
        """
        return {
            'id' : self.id,
            'center' : self.center + [(self.max_altitude + self.min_altitude) / 2],
            'min-bound' : self.min + [self.min_altitude],
            'max-bound' : self.max + [self.max_altitude],
            'geo-origin' : self.base,
        }
    
    def make_link(self, resource_type):
        """
        Generates a download link for the specified resource type.

        Args:
            resource_type (ResourceType): The type of resource (either ResourceType.MESH or ResourceType.PCD).

        Returns:
            str: The download link for the specified resource type.

        Raises:
            ValueError: If the UID does not exist.
        """
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
        """
        Converts the minimum and maximum values to a range string.

        Returns:
            str: The range string in the format "min-max".
        """
        return f"{self.min}-{self.max}"
