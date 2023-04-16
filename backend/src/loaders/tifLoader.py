from typing import Optional
import numpy as np
from geotiff import GeoTiff
from geopy import distance
from multiprocessing.pool import ThreadPool
import open3d as o3d
from threading import Lock, Thread
import uuid
import math
import random
import string
import json
import os
import sqlite3 
import queue
import datetime
from datetime import datetime

from src.database.database import database
global scale_
scale_ = 1
THICKNESS = 10
global default_path_
default_path_ = "./"
global global_base_coord_
global_base_coord_ = (-34, 151)

class TifChunk:
    """
    This class is used to transform each small chunk into a point cloud or mesh

    """

    def __init__(self, points : np.ndarray, size : int, lon_array: np.ndarray, lat_array: np.ndarray, onXY : bool, lat_range, lon_range, id = None):
        """
        Param:
            `points`: np array of altitude
            `size`: length and width size
            `lon_array`: np array of longitude
            `lat_array`: np array of latitude
            `onXY`: Whether the coordinates are described as a XY planar coordinate system
            `padding`: In order to connect the surrounding mesh more smoothly, how many surrounding point clouds are used to calculate the mesh. Please feel free to change this number. It is worth noting that if this value is too large, it will consume more performance

        """
        if id is None:
            self.id_ = str(uuid.uuid4())
        else:
            self.id_ = id
        self.points_ = points.astype(np.float32)
        self.size_ = size
        self.lon_array_ = lon_array.astype(np.float32)
        self.lat_array_ = lat_array.astype(np.float32)
        self.onXY_ = onXY
        self.lat_begin_ = lat_range[0]
        self.lat_end_ = lat_range[1]
        self.lon_begin_ = lon_range[0]
        self.lon_end_ = lon_range[1]
        print(lat_range[0], lat_range[1], lon_range[0], lon_range[1])

    def toPointCloud(self, points : np.ndarray = None, visualization : bool = False, save : bool = False) -> o3d.geometry.PointCloud:
        """
        Param:
            `points`: np array of 3d vector, as a replacement for the point cloud inside the chunks
            `visualization`: Whether to visualize the generated point cloud
            `save`: Whether to save the generated point cloud. If True, it will be saved as. pcd file
            `filename` : saved file name. (Do not use, could not interact with `Manager` now(I haven't try). Only can manual loading of files)
        Return:
            o3d.geometry.PointCloud

        convert file to point cloud
        """
        pcd_id = database.execute_in_worker("select pcd from tifs where uid = ?;", [self.id_])[0][0]
        if pcd_id is None:
            if (points is None):
                points = Loader._merge(self.points_, self.lat_array_, self.lon_array_, self.size_)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            pcd.estimate_normals()
            print(points)
            if save:
                o3d.io.write_point_cloud(f"data/pcds/{self.id_}.pcd", pcd)
                database.execute_in_worker("""
                    insert or replace into pcds(uid,expired, last_update, pth) values (? , ?, ?, ?);
                """,
                [self.id_, 365, datetime.today().timestamp(), f"data/pcds/{self.id_}.pcd"])
                database.execute_in_worker("""
                    update tifs set pcd = (select id from pcds where uid = ?) where uid = ?;
                """,
                [self.id_, self.id_])
        else:
            print("FIND CACHED")
            pcd_info = database.execute_in_worker("select * from pcds where id =?;", [pcd_id])[0]
            pcd = o3d.io.read_point_cloud(pcd_info[4])      

        if visualization:
            o3d.visualization.draw_geometries([pcd])
        return pcd

    def toMesh(self, pcd: o3d.geometry.PointCloud = None, points : np.ndarray = None, visualization : bool = False, color : list = [1, 0.706, 0], save : bool = False) -> o3d.geometry.TriangleMesh:
        """
        Param:
            `points`: np array of 3d vector, as a replacement for the point cloud inside the chunks
            `visualization`: Whether to visualize the generated point cloud
            `color`: The color of the mesh surface
            `save`: Whether to save the generated point cloud. If True, it will be saved as .ply file
            `filename` : saved file name. (Do not use, cannot interact with `Manager` now. Only can manual loading of files)
        Return:
            o3d.geometry.TriangleMesh

        convert file to mesh"""
        mesh_id = database.execute_in_worker("select mesh from tifs where uid = ?;", [self.id_])[0][0]
        if mesh_id is None:
            if pcd is None:
                pcd = self.toPointCloud(points)
            print("mesh")
            pcd.estimate_normals()
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth = 10)
            bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(o3d.utility.Vector3dVector(Loader._merge(self.points_[18: -18, 18 : -18], self.lat_array_[18: -18, 18 : -18], self.lon_array_[18: -18, 18 : -18], self.size_- 18 * 2)))
            p_mesh_crop = mesh.crop(bbox)
            if save:
                o3d.io.write_triangle_mesh(f"data/meshes/{self.id_}.ply", p_mesh_crop, print_progress = True)
                database.execute_in_worker("""
                    insert or replace into meshes(uid,expired, last_update, pth) values (? , ?, ?, ?);
                """,
                [self.id_, 365, datetime.today().timestamp(), f"data/meshes/{self.id_}.ply"])
                database.execute_in_worker("""
                    update tifs set mesh = (select id from meshes where uid = ?) where uid = ?;
                """,
                [self.id_, self.id_])
        else:
            print("FIND CACHED")
            mesh_info = database.execute_in_worker("select * from meshes where id =?;", [mesh_id])[0]
            p_mesh_crop = o3d.io.read_triangle_mesh(mesh_info[4])

        if visualization:
            p_mesh_crop.compute_vertex_normals()
            p_mesh_crop.paint_uniform_color(color)
            o3d.visualization.draw_geometries([p_mesh_crop, bbox,pcd], mesh_show_back_face  = True)
        return p_mesh_crop

def _relativeDistance(given : tuple, base: tuple) -> float:
    """
    return relative distance based on two points.
    """
    distance_ = distance.distance(given, base).m / scale_
    if given[0] < base[0] or given[1] < base[1]:
        return -1 * distance_
    return distance_

def _makeXYPlaneInterp(func, samplingNum: int, array : np.ndarray, base: tuple) -> tuple:
    """
    create mapping
    """
    array = np.unique(array.ravel())
    xp = []
    yp = []
    for row in array.reshape((samplingNum, -1)):
        yp.append(_relativeDistance(func(base, row[0]), base))
        xp.append(row[0])
    yp.append(distance.distance(func(base, array[-1]), base).m / scale_)
    xp.append(array[-1])
    return [np.array(xp), np.array(yp)]

def _mapCoordtoXPPlane(coord, xp: np.ndarray, fp: np.ndarray, size: int) -> tuple:
    """
    map geo coord to xp coord
    """
    return (np.interp(coord.ravel(), xp, fp)).reshape((size, size))

class Loader:
    def __init__(self, filePath : str, origin = None, band:int = 0, as_crs: Optional[int] = 4326, crs_code: Optional[int] = None):
        """
        Param:
            filePath: file path of the .tif file
        """
        self.geo_tiff = GeoTiff(default_path_ + filePath, band, as_crs, crs_code)
        self.filename = filePath.split("/")[-1]
        self.pool_ = ThreadPool(processes= 8)
        self.size_ = self.geo_tiff.tif_shape[0]
        lon_array_raw, lat_array_raw = self.geo_tiff.get_coord_arrays()
        self.id_= str(uuid.uuid4())
        if origin is not None:
            self.origin = origin
        else:
            index = int(self.size_/2)
            self.origin = (lat_array_raw[index][0], lon_array_raw[0][index])
        data = database.execute_in_worker("select uid from tifs where filename = ?;", [self.filename])
        if len(data) == 0:
            database.execute_in_worker(
                """insert or replace into tifs(uid,filename,pth, origin_lat, origin_lon, lat_begin,lat_end, lon_begin,lon_end ) values (? , ?,?, ?, ?, ?, ?, ?, ?);""",
                [self.id_, self.filename, default_path_ + filePath, self.origin[0], self.origin[1], lat_array_raw[0][0], lat_array_raw[-1][0], lon_array_raw[0][0], lon_array_raw[0][-1]]
                )
        else:
            self.id_= data[0][0]


    def read(self) -> np.ndarray:
        """
        Get altitude
        """
        return np.array(self.geo_tiff.read())

    def readWithCoord(self) -> np.ndarray:
        """
        Returns 3D vector according to the geographic coordinates
        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        altitude_array = np.array(self.geo_tiff.read())
        return Loader._merge(altitude_array, lat_array, lon_array, self.size_)

    def readWithXYPlaneCoord(self, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global : bool = False) -> np.ndarray:
        """
        Param:
            `lonSamplingRate` : Sampling number at longitude, i.e. The number of times to sample in a given area
            `latSamplingRate` : Sampling number at latitude, i.e. The number of times to sample in a given area
            `enable_global` : Whether to use the global coordinate system
        Return:
            3d vector of given .tif file

        convert to 3d vector using XY coordinates
        """
        lon_xp_coord, lat_xp_coord = self._covertCoordToXY(self.origin, lonSamplingRate, latSamplingRate, enable_global)
        return Loader._merge(np.array(self.geo_tiff.read()), lat_xp_coord, lon_xp_coord, self.size_)
    
    def toChunkWithXYPlaneCoord(self, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False) -> TifChunk:
        """
        Param:
            `lonSamplingRate` : Sampling number at longitude, i.e. The number of times to sample in a given area
            `latSamplingRate` : Sampling number at latitude, i.e. The number of times to sample in a given area
            `enable_global` : Whether to use the global coordinate system
        Return:
            `TifChunk` of given .tif file

        convert to `TifChunk` using XY coordinates
        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        lon_xp_coord, lat_xp_coord = self._covertCoordToXY(self.origin, lonSamplingRate, latSamplingRate, enable_global)
        return TifChunk(np.array(self.geo_tiff.read()), self.size_, lon_xp_coord, lat_xp_coord, True, (lat_array[0][0], lon_array[-1][0]), (lon_array[0][0], lon_array[0][-1]), self.id_)

    def toChunkWithGeoCoord(self) -> TifChunk :
        """
        convert to `TifChunk` using geographic coordinates

        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        return TifChunk(np.array(self.geo_tiff.read()), self.size_, lon_array, lat_array, (lat_array[0][0], lon_array[-1][0]), (lon_array[0][0], lon_array[0][-1]), self.id_)

    def _covertCoordToXY(self, base, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False) -> tuple:
        """
        map lon and lat to xp plane
        """
        lon_array_raw, lat_array_raw = self.geo_tiff.get_coord_arrays()
        
        lon = self.pool_.apply_async(_makeXYPlaneInterp, args=[lambda base, row: (base[0], row), lonSamplingRate, lon_array_raw, base])
        lat = self.pool_.apply_async(_makeXYPlaneInterp, args=[lambda base, row: (row, base[1]), latSamplingRate, lat_array_raw, base])
        lon_xp, lon_fp = lon.get()
        # Manager().addLonCoordMapping(lon_xp, lon_fp)
        lon = self.pool_.apply_async(_mapCoordtoXPPlane, args=[lon_array_raw, lon_xp, lon_fp, self.size_])
        lat_xp, lat_fp = lat.get()
        # Manager().addLatCoordMapping(lat_xp, lat_fp)
        lat = self.pool_.apply_async(_mapCoordtoXPPlane, args=[lat_array_raw, lat_xp, lat_fp, self.size_])
        lon_xp_coord = lon.get()
        lat_xp_coord = lat.get()
        return (lon_xp_coord, lat_xp_coord)

    @staticmethod
    def setDataDefaultPath(path: str):
        """
        set default path. The default of this is "./"
        """
        global default_path_
        default_path_ = path

    @staticmethod
    def setBaseCoord(coord : tuple):
        """
        set global origin. The default of this is (-34, 151)
        """
        global base_coord_
        base_coord_ = coord
    @staticmethod
    def setScale(scale: float):
        """
        Set the scale of the xy coordinates, the default is 5.
        That is, 1 meter in mesh corresponds to 5 meters in reality.
        Altitude doesn't change
        """
        global scale_
        scale_ = scale

    @staticmethod
    def _merge(altitude_array, lat_array, lon_array, size):
        """
        Composite 3d vector
        """
        r = []
        for i in range(size):
                r.append(np.stack((lat_array[i], lon_array[i], altitude_array[i]), axis = 1))
        return np.array(r).reshape((-1, 3))

    @property
    def crs_code(self):
        return self.geo_tiff.crs_code

    @property
    def as_crs(self):
        return self.geo_tiff.as_crs
    @property
    def tif_shape(self):
        return self.geo_tiff.tif_shape



