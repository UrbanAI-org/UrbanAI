from src.tifProcess.tifLoader import Loader
import matplotlib.pyplot as plt
import open3d as o3d
import threading
import numpy as np
import sys
from src.database.database import database

# database.start()
# # print("database loaded")
# loader = Loader("data/s34_e151_1arc_v3.tif")

# with open('test3.npy', 'wb') as f:
#     np.save(f, loader.readWithXYPlaneCoord().astype(np.int64))
# chunk = loader.toChunkWithXYPlaneCoord()
# chunk.toPointCloud(save=True)
# chunk.toMesh(save=True)
# database.close()
# exit()
mesh_in = o3d.io.read_triangle_mesh("data/meshs/85a6358d-a83c-456c-83e1-571b7a43bc4e.ply")
mesh_in.compute_vertex_normals()
mesh_in.paint_uniform_color([1, 0.706, 0])
box = o3d.geometry.AxisAlignedBoundingBox(np.array([51350.98123502,-45940.86219453, -1000.]), np.array([54899.93582017,-10779.01451035,  3000.        ]))
o3d.visualization.draw_geometries([mesh_in, box])
exit()
# croped_mesh = mesh_in.crop(box)
# o3d.io.write_triangle_mesh(f"chunk.ply", croped_mesh)
# o3d.visualization.draw_geometries([croped_mesh, box])
# exit()
# Manager().clear()
# loader = Loader("data/s34_e151_1arc_v3.tif")

# chunks = loader.toChunkWithXYPlaneCoord()
# mesh = chunks.toMesh()
# o3d.io.write_triangle_mesh(f"total.ply", mesh)
# exit()

# meshs = []
# # for chunk in chunks[0:5]:
# mesh_in = chunks[0].toMesh()
mesh_in = o3d.io.read_triangle_mesh("total.ply")
mesh_in.compute_vertex_normals()
mesh_in.paint_uniform_color([1, 0.706, 0])

# mesh_out = o3d.geometry.crop_triangle_mesh(mesh_in, np.array([11090, -9292, -100]), np.array(0,0, 10000))
mesh_in.triangles = o3d.utility.Vector3iVector(
    np.asarray(mesh_in.triangles)[:len(mesh_in.triangles) // 2, :])
mesh_in.triangle_normals = o3d.utility.Vector3dVector(
    np.asarray(mesh_in.triangle_normals)[:len(mesh_in.triangle_normals) // 2, :])
print(mesh_in.triangles)
# o3d.visualization.draw_geometries([mesh_out])
o3d.visualization.draw_geometries([mesh_in])

exit()

print(
    f'Input mesh has {len(mesh_in.vertices)} vertices and {len(mesh_in.triangles)} triangles'
)
o3d.visualization.draw_geometries([mesh_in])
o3d.io.write_triangle_mesh(f"0.ply", mesh_in)


mesh1 = o3d.geometry.TriangleMesh(mesh_in)
mesh1.triangles = o3d.utility.Vector3iVector(
    np.asarray(mesh1.triangles)[:10000, :])
# mesh1.triangle_normals = o3d.utility.Vector3dVector(
#     np.asarray(mesh1.triangle_normals)[:10000, :])
mesh2 = o3d.geometry.TriangleMesh(mesh_in)
mesh2.triangles = o3d.utility.Vector3iVector(
    np.asarray(mesh2.triangles)[10000:20000, :])
# mesh2.triangle_normals = o3d.utility.Vector3dVector(
#     np.asarray(mesh2.triangle_normals)[10000:20000, :])
print(mesh1.triangles)
o3d.io.write_triangle_mesh(f"0_0_0.ply", mesh1)
o3d.io.write_triangle_mesh(f"0_0_1.ply", mesh2)
mesh1.compute_vertex_normals()
mesh2.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh1, mesh2])


exit()

mesh_out = mesh_in.filter_smooth_laplacian(number_of_iterations=10)
mesh_out.compute_vertex_normals()
print(
    f'Simplified mesh has {len(mesh_out.vertices)} vertices and {len(mesh_out.triangles)} triangles'
)
o3d.visualization.draw_geometries([mesh_out], mesh_show_back_face  = True)
o3d.io.write_triangle_mesh(f"0_0.ply", mesh_out)

voxel_size = max(mesh_in.get_max_bound() - mesh_in.get_min_bound()) / 96
print(f'voxel_size = {voxel_size:e}')
mesh_smp = mesh_in.simplify_vertex_clustering(
    voxel_size=voxel_size,
    contraction=o3d.geometry.SimplificationContraction.Average)
print(
    f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles'
)
o3d.visualization.draw_geometries([mesh_smp], mesh_show_back_face  = True)
o3d.io.write_triangle_mesh(f"1.ply", mesh_smp)

mesh_out = mesh_smp.filter_smooth_laplacian(number_of_iterations=10)
mesh_out.compute_vertex_normals()
print(
    f'Simplified mesh has {len(mesh_out.vertices)} vertices and {len(mesh_out.triangles)} triangles'
)
o3d.visualization.draw_geometries([mesh_out], mesh_show_back_face  = True)
o3d.io.write_triangle_mesh(f"1_0.ply", mesh_out)


# voxel_size = max(mesh_in.get_max_bound() - mesh_in.get_min_bound()) / 256
# print(f'voxel_size = {voxel_size:e}')
# mesh_smp = mesh_in.simplify_vertex_clustering(
#     voxel_size=voxel_size,
#     contraction=o3d.geometry.SimplificationContraction.Average)
# print(
#     f'Simplified mesh has {len(mesh_smp.vertices)} vertices and {len(mesh_smp.triangles)} triangles'
# )
# o3d.visualization.draw_geometries([mesh_smp])
# o3d.io.write_triangle_mesh(f"2.ply", mesh_smp)




Manager().save()