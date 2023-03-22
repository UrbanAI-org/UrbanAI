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

# requirement 
 - flask
 - flask_cors
 - geotiff
 - numpy
 - open3d
 - geopy

# Class 

- TifChunk
    - constructor 
        points : np.ndarray, size : int, lon_array: np.ndarray, lat_array: np.ndarray, onXY, padding = 20
    - toPointCloud
        points = None, visualization = False, save = False, filename = None
    - toMesh
        pcd = None, points = None, visualization = False, color = [1, 0.706, 0], save = False, filename = None
    - read
- Loader:
    - 