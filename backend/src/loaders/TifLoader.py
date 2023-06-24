from typing import Optional
import numpy as np
from geotiff import GeoTiff
from multiprocessing.pool import ThreadPool
import uuid
from src.database.database import database
from src.loaders.utils import makeXYPlaneInterp, mapCoordtoXPPlane,merge
THICKNESS = 10
global default_path_
default_path_ = "./"
# global global_base_coord_
# global_base_coord_ = (-34, 151)





class TifLoader:
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
                [self.id_, self.filename, default_path_ + filePath, self.origin[0], self.origin[1], int(lat_array_raw[0][0]), int(lat_array_raw[-1][0]), int(lon_array_raw[0][0]), int(lon_array_raw[0][-1])]
                )
        else:
            self.id_= data[0][0]


    def read(self) -> np.ndarray:
        """
        Get altitude
        """
        return np.array(self.geo_tiff.read())
    
    def get_id(self):
        return self.id_
    
    def get_geo_coord_lat_lon(self):
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        return lat_array, lon_array

    def get_geo_coord_vectors(self):
        """
        Returns 3D vector according to the geographic coordinates
        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        altitude_array = np.array(self.geo_tiff.read())
        return merge(altitude_array, lat_array, lon_array, self.size_)

    def get_xy_coord_vectors(self, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global : bool = False) -> np.ndarray:
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
        return merge(np.array(self.geo_tiff.read()), lat_xp_coord, lon_xp_coord, self.size_)
    
    def transform_to_xy_coord(self, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False):
        """
        Param:
            `lonSamplingRate` : Sampling number at longitude, i.e. The number of times to sample in a given area
            `latSamplingRate` : Sampling number at latitude, i.e. The number of times to sample in a given area
            `enable_global` : Whether to use the global coordinate system
        Return:
            `TifChunk` of given .tif file

        convert to `TifChunk` using XY coordinates
        """
        # lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        lon_xp_coord, lat_xp_coord = self._covertCoordToXY(self.origin, lonSamplingRate, latSamplingRate, enable_global)
        # return TifChunk(np.array(self.geo_tiff.read()), self.size_, lon_xp_coord, lat_xp_coord, True, (lat_array[0][0], lon_array[-1][0]), (lon_array[0][0], lon_array[0][-1]), self.id_)
        return self.geo_tiff.read(), lat_xp_coord, lon_xp_coord

    def transform_to_geo_coord(self):
        """
        convert to `TifChunk` using geographic coordinates

        """
        lon_array, lat_array = self.geo_tiff.get_coord_arrays()
        # return TifChunk(np.array(self.geo_tiff.read()), self.size_, lon_array, lat_array, (lat_array[0][0], lon_array[-1][0]), (lon_array[0][0], lon_array[0][-1]), self.id_)
        return self.geo_tiff.read(), lat_array, lon_array

    def _covertCoordToXY(self, base, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False) -> tuple:
        """
        map lon and lat to xp plane
        """
        lon_array_raw, lat_array_raw = self.geo_tiff.get_coord_arrays()
        
        lon = self.pool_.apply_async(makeXYPlaneInterp, args=[lambda base, row: (base[0], row), lonSamplingRate, lon_array_raw, base])
        lat = self.pool_.apply_async(makeXYPlaneInterp, args=[lambda base, row: (row, base[1]), latSamplingRate, lat_array_raw, base])
        lon_xp, lon_fp = lon.get()
        # print(lon_xp)
        # print(lon_fp)
        lon = self.pool_.apply_async(mapCoordtoXPPlane, args=[lon_array_raw, lon_xp, lon_fp, self.size_])
        lat_xp, lat_fp = lat.get()
        # print(lat_xp, lat_fp)
        lat = self.pool_.apply_async(mapCoordtoXPPlane, args=[lat_array_raw, lat_xp, lat_fp, self.size_])
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


    @property
    def crs_code(self):
        return self.geo_tiff.crs_code

    @property
    def as_crs(self):
        return self.geo_tiff.as_crs
    @property
    def tif_shape(self):
        return self.geo_tiff.tif_shape



