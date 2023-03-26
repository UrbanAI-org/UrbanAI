import numpy as np 
from geotiff import GeoTiff
from geopy import distance
from multiprocessing.pool import ThreadPool
import open3d as o3d
from threading import Lock, Thread
import math
import random
import string
import json
import os
global scale_
scale_ = 5
THICKNESS = 10
global default_path_
default_path_ = "./"
global global_base_coord_
global_base_coord_ = (-34, 151)

class TifChunk:
    """
    This class is used to transform each small chunk into a point cloud or mesh

    """

    def __init__(self, points : np.ndarray, size : int, lon_array: np.ndarray, lat_array: np.ndarray, onXY : bool, padding : int = 20):
        """
        Param:
            `points`: np array of altitude
            `size`: length and width size
            `lon_array`: np array of longitude
            `lat_array`: np array of latitude 
            `onXY`: Whether the coordinates are described as a XY planar coordinate system
            `padding`: In order to connect the surrounding mesh more smoothly, how many surrounding point clouds are used to calculate the mesh. Please feel free to change this number. It is worth noting that if this value is too large, it will consume more performance
        
        """
        self.id_ = Manager().genID(lat_array[padding: -padding, padding: -padding], lon_array[padding: -padding, padding: -padding], onXY)
        self.points_ = points
        self.size_ = size
        self.lon_array_ = lon_array
        self.lat_array_ = lat_array   
        self.onXY_ = onXY
        self.padding_ = padding

        Manager().addChunk(self.id_, (lat_array[0][0], lat_array[-1][0]), (lon_array[0][0], lon_array[0][-1]), onXY)

    def toPointCloud(self, points : np.ndarray = None, visualization : bool = False, save : bool = False, filename : str = None) -> o3d.geometry.PointCloud:
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
        
        if (points is None):
            points = Loader._merge(self.points_, self.lat_array_, self.lon_array_, self.size_)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.estimate_normals()
        print(points)
        if visualization:
            o3d.visualization.draw_geometries([pcd])
        if save:
            if filename is not None:
                Manager().mapfileNameToId(filename, self.id_)
                filename = self.id_
            o3d.io.write_point_cloud(f"{filename}.pcd", filename)
            Manager().chunkSaved(self.id_, ".pcd")
        return pcd
    
    def toMesh(self, pcd: o3d.geometry.PointCloud = None, points : np.ndarray = None, visualization : bool = False, color : list = [1, 0.706, 0], save : bool = False, filename : str = None) -> o3d.geometry.TriangleMesh:
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
        if Manager().getChunkInfo(self.id_) is not None and Manager().getChunkInfo(self.id_)['saved'] and ".ply" in Manager().getChunkInfo(self.id_)['type']:
            return Manager().getChunkSaved(self.id_, ".ply")
        else:
            if pcd is None:
                pcd = self.toPointCloud(points)
            print("mesh")
            pcd.estimate_normals()
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth = 10)
            bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(o3d.utility.Vector3dVector(Loader._merge(self.points_[18: -18, 18 : -18], self.lat_array_[18: -18, 18 : -18], self.lon_array_[18: -18, 18 : -18], self.size_- 18 * 2)))
            p_mesh_crop = mesh.crop(bbox)
        if visualization:
            p_mesh_crop.compute_vertex_normals()
            p_mesh_crop.paint_uniform_color(color)
            o3d.visualization.draw_geometries([p_mesh_crop, bbox,pcd], mesh_show_back_face  = True)
        if save:
            if filename is not None:
                Manager().mapfileNameToId(filename, self.id_)
                o3d.io.write_triangle_mesh(f"data/meshs/{self.id_}.ply", p_mesh_crop)
            else:
                filename = self.id_
            o3d.io.write_triangle_mesh(f"data/meshs/{filename}.ply", p_mesh_crop)
            Manager().chunkSaved(self.id_, ".ply")
        return p_mesh_crop
    
    
    def toSolidModel(self) -> None:
        """
        DO NOT USE
        """
        pass
    
    def read(self) -> np.ndarray:
        """
        get all 3d vector in chunk
        """
        return Loader._merge(self.points_, self.lat_array_, self.lon_array_, self.size_)
   
    def show(self) -> None:
        """
        show altitude, latitude and longitude coordinate system
        """
        print(self.points_) 
        print(self.lon_array_)
        print(self.lat_array_)

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
        # yp.append(distance.distance(func(base, row[0]), base).m / SCALE)
        xp.append(row[0])
    yp.append(distance.distance(func(base, array[-1]), base).m / scale_)
    xp.append(array[-1])
    return [np.array(xp), np.array(yp)]

def _mapCoordtoXPPlane(coord, xp: np.ndarray, fp: np.ndarray, size: int) -> tuple:
    """
    map geo coord to xp coord
    """
    return (np.interp(coord.ravel(), xp, fp)).reshape((size, size))

def genID():
    """
    DO NOT USE
    """
    return "".join([random.choice(string.ascii_letters) for i in range(0, 13)])

class Loader:
    def __init__(self, filePath : str):
        """
        Param:
            filePath: file path of the .tif file
        """
        self.geo_tiff = GeoTiff(default_path_ + filePath)
        self.pool_ = ThreadPool(processes= 8)
        self.size_ = self.geo_tiff.tif_shape[0]
        random.seed(str(self.geo_tiff.tif_shape))
        Manager().register(self.geo_tiff.tif_bBox)

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
        return Loader.merge(altitude_array, lat_array, lon_array, self.size_)
    
    def cutWithXYPlaneCoord(self, size = 277, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global : bool = False) -> list:
        """
        Param:
            `size`: size of each block
            `lonSamplingRate` : Sampling number at longitude, i.e. The number of times to sample in a given area
            `latSamplingRate` : Sampling number at latitude, i.e. The number of times to sample in a given area
            `enable_global` : Whether to use the global coordinate system
        Return:
            a list of `tifChunk`
        
        Slice using XY coordinates
        """
        lon_xp_coord, lat_xp_coord = self._covertCoordToXY(lonSamplingRate, latSamplingRate, enable_global)
        return self._cutTif(lon_xp_coord, lat_xp_coord, size, onXY = True)
    
    def cutWithCoord(self, size : int = 277) -> list:
        """
         Param:
            `size`: size of each block
        Return:
            a list of `TifChunk`
        
        Slice using geographic coordinates
        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        return self._cutTif(lon_array, lat_array, size)

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
        lon_xp_coord, lat_xp_coord = self._covertCoordToXY(lonSamplingRate, latSamplingRate, enable_global)
        return Loader._merge(np.array(self.geo_tiff.read()), lat_xp_coord, lon_xp_coord, self.size_)
    
    def _cutTif(self, lon: np.ndarray, lat : np.ndarray, size : int = 277, onXY : bool= False, padding : int = 20) -> list:
        """
        to cut into small chunks
        """
        r = []
        altitude_array = np.array(self.geo_tiff.read())
        prew_row = padding
        for row in range(size, self.size_, size):
            prew_col = padding
            for col in range(size, self.size_, size):
                # print(row, col)
                # print(prew_row, prew_col)
                # print(lon)
                # prew_col = col
                # print(lon[prew_row: row, prew_col: col])
                # print(np.size(lon[0]))
                r.append(TifChunk(altitude_array[prew_row - padding: row + padding, prew_col - padding: col+ padding], size, 
                                  lon[prew_row - padding: row+ padding, prew_col- padding: col+ padding], 
                                  lat[prew_row - padding: row+ padding, prew_col- padding: col+ padding], 
                                  onXY)
                                  
                        )
                prew_col = col
            prew_row = row
        r.append(TifChunk(altitude_array[prew_row- padding: , prew_col- padding: ], size, 
                                  lon[prew_row- padding: , prew_col- padding: ], 
                                  lat[prew_row- padding: , prew_col- padding: ], 
                                  onXY)
                                  
                        )
        return r
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
        lon_xp_coord, lat_xp_coord = self._covertCoordToXY(lonSamplingRate, latSamplingRate, enable_global)
        return TifChunk(np.array(self.geo_tiff.read()), self.size_, lon_xp_coord, lat_xp_coord, onXY= True)

    def toChunkWithGeoCoord(self) -> TifChunk :
        """
        convert to `TifChunk` using geographic coordinates
        
        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        return TifChunk(np.array(self.geo_tiff.read()), self.size_, lon_array, lat_array)

    def _covertCoordToXY(self, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False) -> tuple:
        """
        map lon and lat to xp plane
        """
        lon_array_raw, lat_array_raw = self.geo_tiff.get_coord_arrays()
        index = int(self.size_/2)
        if enable_global:
            base = global_base_coord_
        else:
            base = (lat_array_raw[index][0], lon_array_raw[0][index])
        lon = self.pool_.apply_async(_makeXYPlaneInterp, args=[lambda base, row: (base[0], row), lonSamplingRate, lon_array_raw, base])
        lat = self.pool_.apply_async(_makeXYPlaneInterp, args=[lambda base, row: (row, base[1]), latSamplingRate, lat_array_raw, base])
        lon_xp, lon_fp = lon.get()
        Manager().addLonCoordMapping(lon_xp, lon_fp)
        lon = self.pool_.apply_async(_mapCoordtoXPPlane, args=[lon_array_raw, lon_xp, lon_fp, self.size_])
        lat_xp, lat_fp = lat.get()
        Manager().addLatCoordMapping(lat_xp, lat_fp)
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



class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class Range:
    """
    express a range using start and end => [begin, end)
    """
    def __init__(self, begin: float, end : float, round_to : int = 1):
        """
        Param:
            begin: the begining of range
            end: the ending of range
            round_to : round to decimal places
        """
        if begin > end:
            end, begin = begin, end
        self.begin_ = round(begin, round_to)
        self.end_ = round(end, round_to)

    @staticmethod
    def fromString(string: str):
        """
        Create Range from string like "(begin, end)"
        """
        string = string[1:-1]
        nums = string.split(", ")
        return Range(float(nums[0]), float(nums[1]))

    def __eq__(self, another):
        return self.begin_ == another.begin and self.end_ == another.end
    
    def __hash__(self):
        return hash(f"{self.begin_}-{self.end_}")
    
    def __str__(self) -> str:
        return f"[{self.begin_}, {self.end_})"
    
    def __repr__(self) -> str:
        return f"[{self.begin_}, {self.end_})"

    @property
    def begin(self):
        return self.begin_ 
    @property
    def end(self):
        return self.end_
    
class Manager(metaclass=SingletonMeta):
    """
    We'll use this property to prove that our Singleton really works.
    """
    lat_coord_ = {}
    lon_coord_ = {}
    chunks_ = {}
    lat_mapping = [np.array([]), np.array([])]
    lon_mapping = [np.array([]), np.array([])]
    def __init__(self) -> None:
        pass

    def _format_range(self, begin, end):
        if begin > end:
            end, begin = begin, end
        return np.arange(math.floor(begin * 10) / 10, math.ceil(end * 10)/10, 0.1)


    def register(self, bbox):
        """
        Registration lon and lat interval
        """
        lons = self._format_range(bbox[0][0], bbox[1][0])
        # print("lon")
        for lon in lons:
            if Range(lon, lon + 0.1) not in self.lon_coord_:
                # print(Range(lon, lon + 0.1), sep= " ")
                self.lon_coord_.update({Range(lon, lon + 0.1) : []})

        lats = self._format_range(bbox[0][1], bbox[1][1])
        # print("lat")
        for lat in lats:
            # print(Range(lat, lat + 0.1), sep= " ")
            if Range(lat, lat + 0.1) not in self.lat_coord_:
                self.lat_coord_.update({Range(lat, lat + 0.1): []})
    def genID(self, lat, lon, onXY):
        """
        Get the ID of TifChunk
        """
        if onXY:
            lon = np.interp([lon[0][0], lon[-1][-1]], self.lon_mapping[1], self.lon_mapping[0])
            lat = np.interp([lat[0][0], lat[-1][-1]], self.lat_mapping[1], self.lat_mapping[0])
        return f"{lat}-{lon}"
        # lat 35.25 -> 35.38 (35.2 -> 35.4) => (floor(), ceil())
        # lon -30.48 -> -28.33 ( -30.5 -> -28.3)
    def addChunk(self, id : str, lat : np.ndarray, lon : np.ndarray, onXY : bool = False):
        """
        add chunks to manager
        """
        if onXY:
            lon = np.interp(lon, self.lon_mapping[1], self.lon_mapping[0])
            lat = np.interp(lat, self.lat_mapping[1], self.lat_mapping[0])
        lons = self._format_range(lon[0], lon[1])
        for each in lons:
            self.lon_coord_[Range(each, each + 0.1)].append(id)
        lats = self._format_range(lat[0], lat[1])
        for each in lats:
            self.lat_coord_[Range(each, each + 0.1)].append(id)
        self.chunks_[id] = ({"saved": False, "type": []})
        
    def chunkSaved(self, id: str, type: str):
        """
            Tell the manager that already saved the file.
        """
        self.chunks_[id].update({"saved": True})
        if type not in self.chunks_[id]['type']:
            self.chunks_[id]['type'].append(type)

    def mapfileNameToId(self, name, id):
        """
        
        """
        self.chunks_[id].update({"filename": name})
        pass

    def searchChunk(self, polygon : list) -> list:
        """
        Param:
            `polygon`: A list of latitude and longitude coordinates
        Return:
            A list of Ids
        Search for the corresponding chunks by the given coordinates
        """
        lats = [row[0] for row in polygon]
        lons = [row[1] for row in polygon]
        lonRange = (min(lons), max(lons))
        latRange = (min(lats), max(lats))
        lons = self._format_range(lonRange[0], lonRange[1])
        lonPossible = set()
        for each in lons:
            print(Range(each, each + 0.1))
            lonPossible.update(self.lon_coord_[Range(each, each + 0.1)])
        lats = self._format_range(latRange[0], latRange[1])
        latPossible = set()
        for each in lats:
            print(Range(each, each + 0.1))
            latPossible.update(self.lat_coord_[Range(each, each + 0.1)])
        ids = lonPossible.intersection(latPossible)
        return list(ids)
    
    def addLonCoordMapping(self, geo : np.ndarray, xp: np.ndarray):
        """
        Add mapping
        """
        self.lon_mapping[0] = np.sort(np.concatenate((self.lon_mapping[0], geo)))
        self.lon_mapping[1] = np.sort(np.concatenate((self.lon_mapping[1], xp)))

    def addLatCoordMapping(self, geo : np.ndarray, xp: np.ndarray):
        """
        Add mapping
        """
        self.lat_mapping[0] = np.sort(np.concatenate((self.lat_mapping[0], geo)))
        self.lat_mapping[1] = np.sort(np.concatenate((self.lat_mapping[1], xp)))
        
    
    def save(self, path = "./", tempname = ""):
        """
        Param:
            `path`: File save path, the default is the current path
            `tempname`: temporary name for debug or somewhere eles.
        save `Manager`
        """
        with open(path + tempname+ 'config.json', 'w') as outfile:
            json.dump(json.dumps(self.__dict__()), outfile)

    def load(self, path = "./", tempname = ""):
        """
        Param:
            `path`: File save path, the default is the current path
            `tempname`: temporary name for debug or somewhere eles.
        load `Manager`
        """
        with open(path + tempname + 'config.json', 'r') as json_file:
            data = json.loads(json.load(json_file))
            print(type(data))
            self.lat_coord_ = {Range.fromString(key) : value for key, value in data['lat_coord_'].items()}
            self.lon_coord_ = {Range.fromString(key) : value for key, value in data['lon_coord_'].items()}
            self.chunks_ = data['chunks_']
            self.lat_mapping = [
                np.array(data['lat_mapping'][0]),
                np.array(data['lat_mapping'][1])
            ]
            self.lon_mapping = [
                np.array(data['lon_mapping'][0]),
                np.array(data['lon_mapping'][1])
            ]
        
    def tojson(self) -> str:
        """
        convert Manager to json string
        """
        return json.dumps(self.__dict__())
    
    def clear(self):
        """
        clear Manager
        """
        self.lat_coord_ = {}
        self.lon_coord_ = {}
        self.chunks_ = {}
        self.lat_mapping = [np.array([]), np.array([])]
        self.lon_mapping = [np.array([]), np.array([])]

    def __dict__(self):
        """
        convert Manager to jdict
        """
        return {
            "lat_coord_" : {str(key) : value for key, value in self.lat_coord_.items()},
            "lon_coord_" : {str(key) : value for key, value in self.lon_coord_.items()},
            "chunks_" : self.chunks_,
            "lat_mapping" : [self.lat_mapping[0].tolist(), self.lat_mapping[1].tolist(),],
            "lon_mapping" : [self.lon_mapping[0].tolist(), self.lon_mapping[1].tolist(),]
        }

    def getChunkInfo(self, id : str):
        """
        Param:
            `id` : the id of chunk
        get file storage information of given id
        """
        try:
            return self.chunks_[id]
        except KeyError:
            return None
        
    def getChunkSaved(self, Cid : str, Ctype : str):
        """
        Param:
            `Cid`: chunk id
            `Ctype` : saved file type
        get stored file content
        """
        try:
            if self.chunks_[Cid]['saved'] and Ctype in self.chunks_[Cid]['type']:
                if Ctype  == ".ply":
                   return o3d.io.read_triangle_mesh("data/meshs/" + Cid + Ctype)
                if Ctype  == ".pcd":
                   return o3d.io.read_triangle_mesh("data/meshs/" + Cid + Ctype)

        except KeyError:
            return None
    def getChunkSavedURL(self, Cid : str, Ctype: str):
        """
        Param:
            `Cid`: chunk id
            `Ctype` : saved file type
        get stored file path or URL
        """
        try:
            if self.chunks_[Cid]['saved'] and Ctype in self.chunks_[Cid]['type']:
                if Ctype  == ".ply":
                   return os.path.abspath("data/meshs/" + Cid + Ctype)
                if Ctype  == ".pcd":
                   return os.path.abspath("data/meshs/" + Cid + Ctype)

        except KeyError as er:
            print(er)
            return None