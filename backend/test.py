import open3d as o3d 
import numpy as np
from src.database.database import database
# database.start()
# print(database.fetchall("select pth from meshes;"))
# database.close()
file = "data/meshes/f8547cb7-6c9a-47f3-b897-da56cb2b199c.ply"
mesh = o3d.io.read_triangle_mesh(file)
o3d.visualization.draw_geometries([mesh])
# pcd = o3d.io.read_point_cloud(file)
# pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
# o3d.io.write_point_cloud("test.pcd", pcd,print_progress=True, compressed =True  )
# pcd2 = o3d.io.read_point_cloud("test.pcd")
# pcd2.estimate_normals()
# o3d.geometry.
# file1 = "7603cfd2-c24e-494b-9315-c81f92c06231.pcd"
# pcds = [
#     # "f7224a67-939d-43f3-badf-a0d054254d92.pcd",
#     "1e354e32-49cd-447a-8fe4-bc02f93486d9.pcd"
# # "5dfd9494-8926-4f6d-8ede-c8907502f450.pcd",
# # "8a6e30e8-103c-4b33-b285-d34c3bf811c7.pcd",
# # "9383ec7f-12da-4942-9353-8a8063ee1293.pcd",
# # "f7224a67-939d-43f3-badf-a0d054254d92.pcd",
# ]
# # file2 = "251598ae-c85b-44e8-a516-6913c14c104b.pcd"
# # pcds = ["251598ae-c85b-44e8-a516-6913c14c104b.pcd",
# # "30019a1d-f1d3-451a-9657-02432329532a.pcd",
# # "39d09ac0-ac27-4a49-a211-67676bd178dd.pcd",
# # "3db980b9-fc49-4e23-9f5c-1b13f0492a74.pcd",
# # "82072467-406f-439d-a9ab-27560b16a096.pcd",
# # "8310b743-0cc5-4749-8bae-5474155a5711.pcd",
# # "b68d9d86-c5ca-444f-b126-25c281cb7714.pcd",
# # "c8f5fb49-9ed3-4c99-a8cb-868276eed474.pcd",
# # "ddf1aa65-b4d6-4daf-92d0-eb73d0f3249e.pcd",
# # "e63bdf62-1ca1-484a-89fc-7de3627cddb4.pcd",]
# # pcd1 = o3d.io.read_point_cloud("data/pcds/" + file1)
# # pcd2 = o3d.io.read_point_cloud("data/pcds/" + file2)
# # bbox1 = pcd1.get_axis_aligned_bounding_box()
# # bbox2 = pcd2.get_axis_aligned_bounding_box()

# def expand_point_cloud(point_cloud, expansion_distance):
#     # Extract XY coordinates
#     xy_coordinates = np.array(point_cloud.points)[:, :2]

#     # Compute the minimum and maximum values along each axis
#     min_x, min_y = np.min(xy_coordinates, axis=0)
#     max_x, max_y = np.max(xy_coordinates, axis=0)

#     # Create a bounding box around the point cloud
#     expanded_min_x = min_x - expansion_distance
#     expanded_min_y = min_y - expansion_distance
#     expanded_max_x = max_x + expansion_distance
#     expanded_max_y = max_y + expansion_distance

#     # Generate a grid of points within the expanded bounding box
#     x_coords = np.arange(expanded_min_x, expanded_max_x, expansion_distance)
#     y_coords = np.arange(expanded_min_y, expanded_max_y, expansion_distance)
#     expanded_xy = np.meshgrid(x_coords, y_coords).reshape(2, -1).T
#     expanded_z = np.repeat(np.max(point_cloud.points[:, 2]), expanded_xy.shape[0])

#     expanded_points = np.column_stack((expanded_xy, expanded_z))
#     # np.column_stack((xx.flatten(), yy.flatten(), np.zeros_like(xx).flatten()))

#     # Create a new point cloud with the expanded points
#     expanded_cloud = o3d.geometry.PointCloud()
#     expanded_cloud.points = o3d.utility.Vector3dVector(expanded_points)

#     # Merge the original point cloud with the expanded point cloud
#     merged_cloud = o3d.geometry.PointCloud()
#     merged_cloud.points = o3d.utility.Vector3dVector(np.vstack((point_cloud.points, expanded_cloud.points)))

#     return merged_cloud

# pcd_m = [o3d.io.read_point_cloud("data/pcds/" + pcd) for pcd in pcds]
# # o3d.visualization.draw_geometries(pcd_m)
# for pcd in pcd_m:
#     # downpcd = pcd.voxel_down_sample(voxel_size=10)
#     bbox = pcd.get_axis_aligned_bounding_box()
#     # bbox.scale(0.99, bbox.get_center())
#     bbox.color = [1, 0.706, 0]
#     downpcd = pcd
#     downpcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
#     downpcd.estimate_normals()
#     # downpcd.remove_radius_outlier(1, 150)
#     # o3d.visualization.draw_geometries([downpcd, bbox])
#     # expand = expand_point_cloud(pcd, 10)
#     # o3d.visualization.draw_geometries([expand, bbox])
#     mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(downpcd)
#     # bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd.points)
#     # croped_mesh = mesh.crop(bbox)
#     croped_mesh = mesh
#     croped_mesh.compute_vertex_normals()
#     croped_mesh.paint_uniform_color([1, 0.706, 0])
#     o3d.visualization.draw_geometries([croped_mesh, bbox])


# # o3d.visualization.draw_geometries([pcd1])
# # for pcd in pcds:
# #     pcd = o3d.io.read_point_cloud("data/pcds/" + pcd)
# #     bbox = pcd.get_axis_aligned_bounding_box()
# #     o3d.visualization.draw_geometries([pcd, bbox])
    
    
