import open3d as o3d 
# o3d.geometry.
# file1 = "7603cfd2-c24e-494b-9315-c81f92c06231.pcd"
pcds = [
    "f7224a67-939d-43f3-badf-a0d054254d92.pcd",
# "5dfd9494-8926-4f6d-8ede-c8907502f450.pcd",
# "8a6e30e8-103c-4b33-b285-d34c3bf811c7.pcd",
# "9383ec7f-12da-4942-9353-8a8063ee1293.pcd",
# "f7224a67-939d-43f3-badf-a0d054254d92.pcd",
]
# file2 = "251598ae-c85b-44e8-a516-6913c14c104b.pcd"
# pcds = ["251598ae-c85b-44e8-a516-6913c14c104b.pcd",
# "30019a1d-f1d3-451a-9657-02432329532a.pcd",
# "39d09ac0-ac27-4a49-a211-67676bd178dd.pcd",
# "3db980b9-fc49-4e23-9f5c-1b13f0492a74.pcd",
# "82072467-406f-439d-a9ab-27560b16a096.pcd",
# "8310b743-0cc5-4749-8bae-5474155a5711.pcd",
# "b68d9d86-c5ca-444f-b126-25c281cb7714.pcd",
# "c8f5fb49-9ed3-4c99-a8cb-868276eed474.pcd",
# "ddf1aa65-b4d6-4daf-92d0-eb73d0f3249e.pcd",
# "e63bdf62-1ca1-484a-89fc-7de3627cddb4.pcd",]
# pcd1 = o3d.io.read_point_cloud("data/pcds/" + file1)
# pcd2 = o3d.io.read_point_cloud("data/pcds/" + file2)
# bbox1 = pcd1.get_axis_aligned_bounding_box()
# bbox2 = pcd2.get_axis_aligned_bounding_box()
pcd_m = [o3d.io.read_point_cloud("data/pcds/" + pcd) for pcd in pcds]
o3d.visualization.draw_geometries(pcd_m)
# o3d.visualization.draw_geometries([pcd1])
# for pcd in pcds:
#     pcd = o3d.io.read_point_cloud("data/pcds/" + pcd)
#     bbox = pcd.get_axis_aligned_bounding_box()
#     o3d.visualization.draw_geometries([pcd, bbox])
    
    
