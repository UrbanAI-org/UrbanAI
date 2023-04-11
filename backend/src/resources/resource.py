from src.database.database import database
import open3d as o3d
import uuid
from datetime import datetime
# def load_source(id):
#     pth = load_from_meshes(id)
    
class ResourceFetcher:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def load_from_meshes(uid):
        qry = """
        select pth from meshes where uid = ?;
        """
        data = database.execute_in_worker(qry, [uid])
        if len(data) == 0:
            return None
        else:
            return data[0][0]
        
    @staticmethod
    def load_from_pcds(uid):
        qry = """
        select pth from pcds where uid = ?;
        """
        data = database.execute_in_worker(qry, [uid])
        if len(data) == 0:
            return None
        else:
            return data[0][0]
    

    # {
    #                 "chunk_id" : self.id,
    #                 "type" : type
    #             }
# def process_request(process, chunk):
#     if request['type'] == 'mesh':
#         process_mesh(request['chunk_id'])
#     elif request['type'] == 'pcd':
#         process_pcd(request['chunk_id'])

# def process_pcd(chunk):
#     qry = """
#     select pth from pcds where uid = ?;
#     """
#     data = database.execute_in_worker(qry, [chunk.parent])[0]
#     pcd = o3d.io.read_point_cloud(data[0])
#     croped_pcd = pcd.crop(chunk.to_bbox())
#     pcd_id = str(uuid.uuid4())
#     o3d.io.write_point_cloud(f"data/pcds/{pcd_id}.pcd", croped_pcd, print_progress = True)
#     qry = """
#         insert or replace into pcds(uid, expired, last_update, pth) 
#         values (?,?,?,?);
#         """
#     database.execute_in_worker(qry, [pcd_id, 3, datetime.now().timestamp(), f"data/pcds/{pcd_id}.pcd"])
#     qry = """
#         update chunks set pcd = (select id from pcds where uid = ?) where id = ?;
#     """
#     database.execute_in_worker(qry, [pcd_id, chunk.id])
#     pass 

# def process_mesh(chunk):
#     qry = """
#     select pth from meshes where uid = ?;
#     """
#     data = database.execute_in_worker(qry, [chunk.parent])[0]
#     mesh = o3d.io.read_triangle_mesh(data[0])
#     print(
#     f'Input mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles'
#     )
    
#     croped_mesh = mesh.crop(chunk.to_bbox())
#     print(
#     f'Input mesh has {len(croped_mesh.vertices)} vertices and {len(croped_mesh.triangles)} triangles'
#     )
#     if len(croped_mesh.triangles) == 0:
#         return
#     # return
#     mesh_id = str(uuid.uuid4())
#     o3d.io.write_triangle_mesh(f"data/meshs/{mesh_id}.ply", croped_mesh, print_progress = True)
#     qry = """
#         insert or replace into meshes(uid, expired, last_update, pth) 
#         values (?,?,?,?);
#         """
#     database.execute_in_worker(qry, [mesh_id, 3, datetime.now().timestamp(), f"data/meshs/{mesh_id}.ply"])
#     qry = """
#         update chunks set mesh = (select id from meshes where uid = ?) where id = ?;
#     """
#     database.execute_in_worker(qry, [mesh_id, chunk.id])


