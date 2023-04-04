# from osgeo import gdal
import matplotlib.pyplot as plt
from geotiff import GeoTiff
import numpy as np
import open3d as o3d
from multiprocessing.pool import ThreadPool
from collections import deque
from geopy import distance
import datetime
import random
import threading
from multiprocessing.pool import ThreadPool
# for i in range(100000):
#     newport_ri = (random.randint(-90, 90), random.randint(-90, 90))
#     cleveland_oh = (random.randint(-90, 90), random.randint(-90, 90))
#     # print(distance.distance(newport_ri, cleveland_oh).miles)
# after = datetime.datetime.now()
# print(after - before)
# exit()
geo_tiff = GeoTiff('data/s34_e151_1arc_v3.tif')
# the original crs code
print(geo_tiff.crs_code)
# exit()

# the current crs code
print(geo_tiff.as_crs)
# the shape of the tiff
print(geo_tiff.tif_shape)
# the bounding box in the as_crs CRS
print(geo_tiff.tif_bBox)
# the bounding box as WGS 84
print(geo_tiff.tif_bBox_wgs_84)
# the bounding box in the as_crs converted coordinates
print(geo_tiff.tif_bBox_converted)
lon_array_raw, lat_array_raw = geo_tiff.get_coord_arrays()
print(lon_array_raw, lat_array_raw)
exit()
def mytry(array, base):
    array = np.unique(array.ravel())
    a = [] 
    b = []
    for lon in array.reshape((277, -1)):
        a.append(distance.distance((base[0], lon[0]), base).m)
        b.append(lon[0])
    return (np.array(b), np.array(a))
before = datetime.datetime.now()

# lon_array = np.unique(lon_array_raw.ravel())
# lat_array = np.unique(lat_array_raw.ravel())
index = int(3601/2)
base = (lat_array_raw[index][0], lon_array_raw[0][index])
print(base)
# base = (lat_array[index], lon_array[index])
# print(base)
pool = ThreadPool(processes= 8)
taska = pool.apply_async(mytry, args=[lon_array_raw, base])
taskb = pool.apply_async(mytry, args=[lat_array_raw, base])
# taska = threading.Thread(target=mytry, args=[lon_array, base])
# taskb = threading.Thread(target=mytry, args=[lat_array, base])
# taska.start()
# taskb.start()
xp, fp = taska.get()
taskb.get()
# print(res)
# taskb.join()
# print(xp, fp)
def myfunc(elem):
    return np.interp(elem, xp, fp)

# def multiInterp2(x, xp, fp):
#     i = np.arange(x.size)
#     j = np.searchsorted(xp, x) - 1
#     print(i, j)
#     d = (x - xp[j]) / (xp[j + 1] - xp[j])
#     return (1 - d) * fp[i, j] + fp[i, j + 1] * d

# for row in lon_array_raw:
#     a = multiInterp2(row, xp, fp)
#     print(a)
# a = np.vectorize(myfunc)(lon_array_raw)
# print(a)
print("AAAA")
# ps = []
# for row in range(3601):
ps = (np.interp(lon_array_raw.ravel(), xp, fp)).reshape((3601, 3601))
    # for col in range(3601):
print(ps)
after = datetime.datetime.now()
print(after - before)
# geo_tiff.get_int_box()
# print(lon_array, lat_array)
# print(index)
# print(lon_array.reshape((13, -1)))

# for lon in lon_array.reshape((13, -1)):
#     distance.distance((base[0], lon[0]), base)
# for lat in lat_array.reshape((13, -1)):
#     distance.distance((lat[0], base[1]), base)
# zarr_array = geo_tiff.read()
# # read tiff data
# array = np.array(zarr_array)
# print(array)
exit()
array = geo_tiff.read_box(geo_tiff.tif_bBox)
print(array)
geo_tiff
# exit()

# visualization the tiff file 
plt.imshow(array, interpolation='none', cmap='gist_gray')
plt.show()





# exit()
# --------------------------------------------
# if we assume that the value in array is the altitude of given position.
# Output visualization for each SKIP point. If SKIP = 1, output every point, if SKIP = 2, output every two points.
SKIP = 1
pool = ThreadPool(processes=40)

# add_array(*args) trans(*args):
# convert np.array() 
# [[1,1,1,1,1,], [1,1,1,1,1,], ...,[1,1,1,1,1,]] 
# => 
# [[0,0,z], [0,1,1], ...., [n, n-1, 1], [n,n,1]]

x = -36
y = -36
step = 1/ 3601

def add_array(col, rows, array):
    temp = np.empty((rows, 3))
    row = 0
    while row < rows: 
        temp[row] = np.array([row * step, col, array[row]])
        row += SKIP
    return temp

def trans(cols, rows, array):
    queue = deque([])
    col = 0
    while col < cols:
    # for col in range(cols):
        task = pool.apply_async(add_array, (col, rows, array[col]))
        queue.append(task)
        col += SKIP
    print("DONE TASKS", len(queue))
    buf = np.array(queue.popleft().get())
    while len(queue) != 0:
        ele = queue.popleft().get()
        buf = np.concatenate((buf, ele), axis=0)
    return buf


# output 200 * 100 points
buf = trans(200, 100, array)
# output 500 * 100 points
# buf2 = trans(500, 500, array)

# convert np array into PointCloud
pcd = o3d.geometry.PointCloud()
pcd2 = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(buf)
# pcd2.points = o3d.utility.Vector3dVector(buf2)

print("Generate TriangleMesh ...")

# pcd2.estimate_normals()

# transfer pointcloud to mesh surfaces
tr_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd)

# remove box borders
bbox = pcd.get_axis_aligned_bounding_box()
p_mesh_crop = tr_mesh[0].crop(bbox)
print("Generate TriangleMesh Done.")

# visualization
o3d.visualization.draw_geometries([p_mesh_crop, pcd])