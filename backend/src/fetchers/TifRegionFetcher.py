import numpy as np
from src.loaders.utils import merge
import open3d as o3d
import uuid
import src.fetchers.ResourceFetcher as ResourceFetcher
from src.fetchers.FetchersConsts import ResourceAttr
from src.database.database import database


class TifRegionFetcher:
    def __init__(self, points: np.ndarray, lat_array: np.ndarray, lon_array: np.ndarray, id=None) -> None:
        """
        Initialize a TifRegionFetcher object.

        Parameters:
        - points (np.ndarray): Array of points.
        - lat_array (np.ndarray): Array of latitude values.
        - lon_array (np.ndarray): Array of longitude values.
        - id (optional): Identifier for the object.

        Returns:
        None
        """
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
        self.crop_pcd = False
        pass
    
    def _set_geo_range(self, lat_array, lon_array):
        """
        Set the geographic range based on the given latitude and longitude arrays.

        Args:
            lat_array (numpy.ndarray): Array of latitude values.
            lon_array (numpy.ndarray): Array of longitude values.
        """
        self.lat_begin_ = np.amin(lat_array)
        self.lat_end_ = np.amax(lat_array)
        self.lon_begin_ = np.amin(lon_array)
        self.lon_end_ = np.amax(lon_array)

    @staticmethod
    def create_by_loader(loader, by="xy"):
        """
        Create a TifRegionFetcher object based on the given loader.

        Args:
            loader (Loader): The loader object used to create the TifRegionFetcher.
            by (str, optional): The coordinate system to use for creating the TifRegionFetcher.
                Valid values are "xy" (default) or "geo".

        Returns:
            TifRegionFetcher: The created TifRegionFetcher object.

        Raises:
            ValueError: If the `by` parameter is not set to "xy" or "geo".
        """
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
        """
        Updates the database with the PCD and mesh values for the current object.

        Parameters:
            None

        Returns:
            None
        """
        qry = f"""
            update tifs set pcd = ?, mesh = ? where uid=?;
        """
        database.execute_in_worker(qry, [self.pcd, self.mesh, self.id_])

    def load_resource_from_database(self):
        """
        Load the mesh and point cloud data from the database based on the unique identifier (uid).
        """
        qry = """
            select mesh, pcd from tifs where uid = ?
        """
        mesh, pcd = database.fetchone(qry, [self.id_])
        self.mesh = mesh 
        self.pcd = pcd

    def make_pcd(self, crop=False, num=0):
        """
        Converts the points, latitude, longitude, and size arrays into a point cloud (PCD) object.
        
        Args:
            crop (bool): Flag indicating whether to crop the point cloud.
            num (int): Number of points to keep if cropping is enabled.
        
        Returns:
            o3d.geometry.PointCloud: The generated point cloud object.
        """
        fetcher = ResourceFetcher.PcdResourceFetcher()
        if self.pcd is None:
            print("make PCD")
            vectors = merge(self.points_, self.lat_array_, self.lon_array_, self.size_)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(vectors)
            pcd.estimate_normals()
            if crop and num > 0:
                self.crop_pcd = True
                self._crop_pcd(pcd, num)
            else:
                path = f"data/pcds/{self.id_}.pcd"
                o3d.io.write_point_cloud(f"data/pcds/{self.id_}.pcd", pcd, print_progress=True)
                self.pcd = fetcher.write_to_database(self.id_, path)
            self.update_database()
        else:
            # TODO: READ PCD FROM MUTIPLE FILES
            pth = fetcher.get_pth(ResourceAttr.UNIQUE_ID, self.id_)
            pcd = o3d.io.read_point_cloud(pth)
        return pcd

    def make_mesh(self, depth = 10):
        """
        Creates a mesh from the point cloud data.

        Args:
            depth (int): The depth parameter for the Poisson surface reconstruction algorithm.

        Returns:
            o3d.geometry.TriangleMesh: The cropped triangle mesh.
        """
        pcd = self.make_pcd()
        fetcher = ResourceFetcher.MeshResourceFetcher()
        if self.mesh is None:
            print("make MESH")
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth = depth)
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
    
    def _crop_pcd(self, pcd, num):
        """
        Crop the point cloud data (pcd) to a specified number of points (num).
        Haven't been implemented yet.
        Args:
            pcd (PointCloud): The input point cloud data.
            num (int): The desired number of points to crop the point cloud to.

        Returns:
            None
        """
        pass

    #     max_bound = pcd.get_max_bound()
    #     min_bound = pcd.get_min_bound()
    #     diff = (max_bound - min_bound) / num


