# Server API
```
POST /query/mesh

data: {
    [
            (-33.005, 151.0056),
            (-33.021, 151.078),
            (-33.037, 151.384),
        ]
}
response : {
    [
        '/home/shilong/urbanAI/UrbanAI/backend/src/data/meshs/[-33.00555556 -33.07666667]-[151.30777778 151.38444444].ply',
        '/home/shilong/urbanAI/UrbanAI/backend/src/data/meshs/[-33.00555556 -33.07666667]-[151.23083333 151.3075    ].ply',
        '/home/shilong/urbanAI/UrbanAI/backend/src/data/meshs/[-33.00555556 -33.07666667]-[151.00555556 151.07666667].ply',
        '/home/shilong/urbanAI/UrbanAI/backend/src/data/meshs/[-33.00555556 -33.07666667]-[151.15388889 151.23055556].ply',
        '/home/shilong/urbanAI/UrbanAI/backend/src/data/meshs/[-33.00555556 -33.07666667]-[151.07694444 151.15361111].ply'
    ]
}
```
This API returns only the map within the selected area for which the ply has been generated. This will automatically match the file path on your computer，If our data is in AWS in the future, this can also be replaced with the link of AWS.
It's worth noting that I'm not sure how large the total size of the separate .ply s will be, it could reach hundreds of MB. If you want you can process entire .tif directly, although it may be slower on the front end, you can still get the file path/URL with the above API.



# requirement 
 - flask
 - flask_cors
 - geotiff
 - numpy
 - open3d
 - geopy

# Class 
There is an `example.py` under the src folder, some examples of these classes is written above/
**Note** some default variable value is perfect, such as r'.*?SamplingRate', 
XYPlaneCoord refers to the coordinates in the plane coordinate system. If enable_global is not enabled, the relative coordinate origin is the center of the image, otherwise, coordinate origin is (-34, 151) in geographic coordinates. You can change this coordinate by `setBaseCoord`.

- TifChunk
    - constructor 
        points : np.ndarray, size : int, lon_array: np.ndarray, lat_array: np.ndarray, onXY, padding = 20
    - toPointCloud
        points = None, visualization = False, save = False, filename = None
    - toMesh
        pcd = None, points = None, visualization = False, color = [1, 0.706, 0], save = False, filename = None
    - read
- Loader:
    - constructor
        filePath : str, geoTiff = None
    - read
    - readWithCoord
    - cutWithXYPlaneCoord 
        size = 277, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False
    - cutWithCoord
        size = 277
    - readWithXYPlaneCoord
        lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False

    - toChunkWithXYPlaneCoord
        lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False
    - toChunkWithGeoCoord
    - setBaseCoord
        coord
- Manager
    - register
        bbox
    - searchChunk
        polygon : list
    - save
        path = "./", tempname = ""
    - load
        path = "./", tempname = ""
    - tojson
    - clear
    - getChunkInfo
        id
    - getChunkSaved
        Cid, Ctype
    - getChunkSavedURL
        Cid, Ctype
