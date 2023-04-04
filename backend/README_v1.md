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
This API returns only the map within the selected area for which the ply has been generated. The server cannot obtain the mesh area that has not been generated .ply. This will automatically match the file path on your computer，If our data is in AWS in the future, this can also be replaced with the link of AWS. 

It's worth noting that I'm not sure how large the total size of the separate .ply s will be, it could reach hundreds of MB. If you want you can process entire .tif directly, although it may be slower on the front end, you can still get the file path/URL with the above API.

# Make meshs
Actually, if you have enough disk space and time, you can run the following code, just like in example.py to obtain meshs for all chunks of areas.

.ply will be saved to `./data/meshs`
- load whole directly (the size of .ply is about 90MB)
```py
loader = Loader("data/s34_e151_1arc_v3.tif")
chunk = loader.toChunkWithXYPlaneCoord()
mesh = chunk.toMesh(save=True)
Manager().save()
```
- load chunks (the size of each is about 12MB, The size will be determined according to the number of faces in it. There are 13*13 chunks in total)
```py
loader = Loader("data/s34_e151_1arc_v3.tif")
chunks = loader.cutWithXYPlaneCoord()
meshs = []
for chunk in chunks:
    mesh = chunk.toMesh(save=True)
Manager().save()
```

# Requirements
 - flask
 - flask_cors
 - geotiff
 - numpy
 - open3d
 - geopy

# Class 
There is an `example.py` under the src folder, some examples of these classes is written above

**Note** some default variable value, such as r'.*?SamplingRate'. This number refers to the number of samples for a one-arc geographic coordinate system. For example, if the number is 277, then the latitude and longitude of each image will be divided into 277 pieces to obtain the corresponding xy coordinates. The latitude and longitude in the middle of each block will linearly correspond to a point between the coordinates of the left and right ends.


`XYPlaneCoord` refers to the coordinates in the plane coordinate system. 

If `enable_global` is not enabled, the relative coordinate origin is the center of the image, otherwise, coordinate origin is (-34, 151) in geographic coordinates. You can change this coordinate by `setBaseCoord`.

See the strdoc of the code for more detail
- TifChunk
    - constructor(points : np.ndarray, size : int, lon_array: np.ndarray, lat_array: np.ndarray, onXY, padding = 20)
        
    - toPointCloud(
        points = None, visualization = False, save = False, filename = None)

    - toMesh:
        (pcd = None, points = None, visualization = False, color = [1, 0.706, 0], save = False, filename = None)
    - read:
- Loader:
    - constructor
        (filePath : str, geoTiff = None)
    - read
    - readWithCoord
    - cutWithXYPlaneCoord 
        (size = 277, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False)
    - cutWithCoord
        (size = 277)
    - readWithXYPlaneCoord
        (lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False)

    - toChunkWithXYPlaneCoord
        (lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False)
    - toChunkWithGeoCoord
    - setBaseCoord
        (coord)
- Manager
    - register
        (bbox)
    - searchChunk
        (polygon : list)
    - save
        (path = "./", tempname = "")
    - load
        (path = "./", tempname = "")
    - tojson
    - clear
    - getChunkInfo
        (id)
    - getChunkSaved
        (Cid, Ctype)
    - getChunkSavedURL
        (Cid, Ctype)
