import numpy as np
from src.loaders.utils import merge
import open3d as o3d
import uuid
import src.fetchers.ResourceFetcher as ResourceFetcher
from src.fetchers.FetchersConsts import ResourceAttr
from src.database.database import database
class TifRegionFetcher:
    def __init__(self, points : np.ndarray, lat_array : np.ndarray, lon_array: np.ndarray, id = None) -> None:
        self.points_ = points.astype(np.float32)
        self.size_ = len(points[0])
        self.lon_array_ = lon_array.astype(np.float32)
        self.lat_array_ = lat_array.astype(np.float32)
        self.lat_begin_ = np.amin(lat_array)
        self.lat_end_ = np.amax(lat_array)
        self.lon_begin_ = np.amin(lon_array)
        self.lon_end_ = np.amax(lon_array)
        self.id_ = id
        self.mesh = None
        self.pcd = None
        pass
    
    def _set_geo_range(self, lat_array, lon_array):
        self.lat_begin_ = np.amin(lat_array)
        self.lat_end_ = np.amax(lat_array)
        self.lon_begin_ = np.amin(lon_array)
        self.lon_end_ = np.amax(lon_array)

    @staticmethod
    def create_by_loader(loader, by = "xy"):
        if by == "xy":
            points, lat, lon = loader.transform_to_xy_coord()
            fetcher = TifRegionFetcher(points, lat, lon, id=loader.get_id())
            geo_lat, geo_lon = loader.get_geo_coord_lat_lon()
            fetcher._set_geo_range(geo_lat, geo_lon)
        elif by == "geo":
            points, lat, lon = loader.transform_to_geo_coord()
            fetcher = TifRegionFetcher(points, lat, lon, id=loader.get_id())
        
        else:
            raise ValueError("paramer `by` is expect 'xy' or 'geo'.")
        fetcher.load_resource_from_database()
        return fetcher
    
    def update_database(self):
        qry = f"""
            update tifs set pcd = ?, mesh = ? where uid=?;
        """
        database.execute_in_worker(qry, [self.pcd, self.mesh, self.id_])

    def load_resource_from_database(self):
        qry = """
            select mesh, pcd from tifs where uid = ?
        """
        mesh, pcd = database.fetchone(qry, [self.id_])
        self.mesh = mesh 
        self.pcd = pcd

    def make_pcd(self):
        fetcher = ResourceFetcher.PcdResourceFetcher()
        if self.pcd is None:
            print("make PCD")
            vectors = merge(self.points_, self.lat_array_, self.lon_array_, self.size_)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(vectors)
            pcd.estimate_normals()
            path = f"data/pcds/{self.id_}.pcd"
            o3d.io.write_point_cloud(f"data/pcds/{self.id_}.pcd", pcd, print_progress = True)
            self.pcd = fetcher.write_to_database(self.id_, path)
            self.update_database()
        else:
            pth = fetcher.get_pth(ResourceAttr.UNIQUE_ID, self.id_)
            pcd = o3d.io.read_point_cloud(pth)
        return pcd

    def make_mesh(self):
        pcd = self.make_pcd()
        fetcher = ResourceFetcher.MeshResourceFetcher()
        if self.mesh is None:
            print("make MESH")
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd)
            bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd.points)
            p_mesh_crop = mesh.crop(bbox)
            path = f"data/meshes/{self.id_}.ply"
            fetcher = ResourceFetcher.MeshResourceFetcher()
            o3d.io.write_triangle_mesh(f"data/meshes/{self.id_}.ply", p_mesh_crop, print_progress = True)
            self.mesh = fetcher.write_to_database(self.id_, path)
            self.update_database()
        else:
            pth = fetcher.get_pth(ResourceAttr.UNIQUE_ID, self.id_)
            p_mesh_crop = o3d.io.read_triangle_mesh(pth)
        return p_mesh_crop
        
