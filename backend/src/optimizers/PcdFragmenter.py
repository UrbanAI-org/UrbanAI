import numpy as np
import open3d as o3d
import uuid

from src.fetchers.ResourceFetcher import PcdResourceFetcher
from src.fetchers.FetchersConsts import ResourceAttr
from datetime import datetime
class Fragmenter:
    uids = []
    n = 1
    database = None
    def __init__(self, uids, database, n=1) -> None:
        """
        Initialize the PcdFragmenter object.

        Args:
            uids (list): List of unique identifiers.
            database (str): Database name.
            n (int, optional): Number of fragments. Defaults to 1.
        """
        self.uids = uids
        self.n = n
        self.database = database

    def is_already_optimized(self):
        """
        Check if the data has already been optimized.

        Returns:
            bool: True if the data has already been optimized, False otherwise.
        """
        pass

    def execute(self):
        """
        Executes the PcdFragmenter algorithm.

        This method reads point clouds, splits them into blocks, and inserts the fragmented blocks into the database.
        Haven't test this yet.

        Returns:
            None
        """
        fetcher = PcdResourceFetcher()
        max = len(self.uids)
        curr = 0
        for uid in self.uids:
            before = datetime.now()
            id = fetcher.get_db_id(ResourceAttr.UNIQUE_ID, uid)
            pcd = o3d.io.read_point_cloud(f"data/pcds/{uid}.pcd")
            if pcd.is_empty():
                curr += 1
                continue
            blocks = self._split_point_cloud(pcd)
            for block in blocks:
                qry = f"""
                insert into fragmented_pcds(min_bound_x, min_bound_y, max_bound_x, max_bound_y, parent, pth, parent_id) values ({",".join("?" * 7)});
                """
                self.database.execute_in_worker(qry, [
                    block['min'][0], block['min'][1],
                    block['max'][0], block['max'][1],
                    uid, block['pth'], id
                ])
            empty_pcd = o3d.geometry.PointCloud()
            print(f"Empty the file: {uid}.pcd")
            o3d.io.write_point_cloud(f"data/pcds/{uid}.pcd", empty_pcd)
            after = datetime.now()
            curr += 1
            print("Estimate time left", (after - before) * (max - curr))


    def _split_point_cloud(self, point_cloud):
        """
        Splits a point cloud into smaller blocks based on the specified number of divisions.
        Haven't test this yet.

        Args:
            point_cloud (o3d.geometry.PointCloud): The input point cloud.

        Returns:
            list: A list of dictionaries, where each dictionary contains the maximum and minimum bounds
                    of a block, as well as the file path where the block is saved.
        """
        points = np.asarray(point_cloud.points)
        x_coords = points[:, 0]
        y_coords = points[:, 1]
        x_range = np.max(x_coords) - np.min(x_coords)
        y_range = np.max(y_coords) - np.min(y_coords)
        block_size_x = x_range / self.n
        block_size_y = y_range / self.n
        split_point_clouds = []
        for i in range(self.n):
            for j in range(self.n):
                min_x = np.min(x_coords) + i * block_size_x
                max_x = min_x + block_size_x
                min_y = np.min(y_coords) + j * block_size_y
                max_y = min_y + block_size_y
                mask = (x_coords >= min_x) & (x_coords < max_x) & (y_coords >= min_y) & (y_coords < max_y)
                block_points = points[mask]

                block_point_cloud = o3d.geometry.PointCloud()
                block_point_cloud.points = o3d.utility.Vector3dVector(block_points)
                max_bound = block_point_cloud.get_max_bound()
                min_bound = block_point_cloud.get_min_bound()
                filename = f"{str(uuid.uuid4())}.pcd"
                print(f"Range [{min_x}, {min_y}] - [{max_x}, {max_y}]")
                o3d.io.write_point_cloud(f"data/pcds/{filename}", block_point_cloud, print_progress=True, compressed =True)
                split_point_clouds.append({
                    "max" : max_bound, 
                    "min" : min_bound,
                    "pth" : f"data/pcds/{filename}"
                })

        return split_point_clouds

