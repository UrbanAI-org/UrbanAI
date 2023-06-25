from src.optimizers.OptimizerInterface import Optimizer
import open3d as o3d 
import numpy as np
from datetime import datetime
class Compresser(Optimizer):
    uids = []
    def __init__(self, uids) -> None:
        self.uids = uids

    def is_already_optimized(self):
        pass
    
    def execute(self):
        max = len(self.uids)
        curr = 0
        for uid in self.uids:
            before = datetime.now()
            print("Open file:", f"data/pcds/{uid}.pcd")
            pcd = o3d.io.read_point_cloud(f"data/pcds/{uid}.pcd")
            if not pcd.is_empty():
                pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
                o3d.io.write_point_cloud(f"data/pcds/{uid}.pcd", pcd,print_progress=True, compressed =True)
            after = datetime.now()
            curr += 1
            print("Estimate time left", (after - before) * (max - curr))
            

    