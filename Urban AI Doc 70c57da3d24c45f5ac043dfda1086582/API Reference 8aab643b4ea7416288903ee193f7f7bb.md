# API Reference

# Classes reference

## class `Database` extends from `SingletonMeta`

A class to serialize qury and provide multi-thread safe access database

### attribute

- work_queue : queue.Queue
- db : str
- tables: str
- dbloop : bool

### method

- init(db :str , tables:str)
    
    create a Database object
    
    Params:
    
    ```
      db: the name of database
    
      tables : the databse schema
    
    ```
    
- start() -> None
    
    connect to database
    
- execute_in_worker(sql : str, params =[]) -> list | None
    
    execute the qury and return the result
    
    Params:
    
    ```
      sql: str the qury need to execute
    
      params : list the paramter need to be passed
    
    ```
    
    Returns:
    
    ```
      list, that contails all result.
    
    ```
    
- fetchall(sql :str, params =[]) -> list | None
    
    execute the qury and return the result
    
    Params:
    
    ```
      sql: str the qury need to execute
    
      params : list the paramter need to be passed
    
    ```
    
    Returns:
    
    ```
      list, that contails all result.
    
    ```
    
- fetchone(sql :str, params =[]) -> list | None
    
    execute the qury and return the result
    
    Params:
    
    ```
      sql: str the qury need to execute
    
      params : list the paramter need to be passed
    
    ```
    
    Returns:
    
    ```
      list, that contails the first line of the result.
    
    ```
    
- close() -> None
    
    close the database.
    

## class `SingletonMeta`

Provide Singleton Abstract class

### attribute

- _instances: dict
- _lock : Lock

## class `RegionDataFetcher`

Process user-defined regions and return resources

### attribute

- center: list
- min: list
- max: list
- base: list
- parent: int
- mesh: int
- pcd: int
- max_altitude: float
- min_altitude: float

### static method

- create_by_polygon(polygon :list, base :list, parent : str)
- create_by_circle(center :list, radius: str | int | float, base:list, parent : str)
- to_XY_Plane(coord:list, base:list)
- read_from_database(id:int)

### method

- write_to_database() -> None
- get_bbox() -> o3d.geometry.AxisAlignedBoundingBox
- get_mesh(encoded = lambda data: base64.b64encode(data).decode("utf-8")) -> str
- get_pcd(encoded = lambda data: base64.b64encode(data).decode("utf-8")) -> str
- make_mesh() -> o3d.geometry.TriangleMesh
- make_pointcloud() -> o3d.geometry.PointCloud
- to_details() -> dict
- make_link(resource_type: ResourceType) -> str

## class `ResourceFetcher` (Abstract Class)

provide a easier way to qury the database for resources.

### attribute

domain : str

### method

- get_pth(by : ResourceAttr, value : any) -> str
- get_content(by: ResourceAttr, value: any) -> BufferedReader
- get_uid(by: ResourceAttr, value: any) -> str
- get_db_id(by: ResourceAttr, value: any) -> int
- _get_attr_by_attr(result: ResourceAttr, by: ResourceAttr, value: any) -> any
- write_to_database(uid:str, path:str, expired = 3) -> None

## class `MeshResourceFetcher` extends from `ResourceFetcher`

provide a easier way to qury the database for meshes.

## class `PcdResourceFetcher` extends from `ResourceFetcher`

provide a easier way to qury the database for pcds.

## class `TifRegionFetcher`

### attribute

points_: np.ndarray
size_: int
lon_array_: np.ndarray
lat_array_: np.ndarray
lat_begin_: float
lat_end_: float
lon_begin_: float
lon_end_: float
id_: str
mesh: int
pcd: int

### static method

- create_by_loader(loader : TifLoader, by = "xy"):

### method

- _set_geo_range(lat_array:np.ndarray, lon_array:np.ndarray)
- update_database() -> None
- load_resource_from_database() -> None
- make_pcd() -> o3d.geometry.PointCloud
- make_mesh() -> o3d.geometry.TriangleMesh

## class `TifLoader`

### attribute

self.geo_tiff: GeoTiff
self.filename: str
self.pool_: ThreadPool
self.size_: int
[self.id](http://self.id/): str
self.origin: list

### static method

- setDataDefaultPath(path: str) -> None
- setBaseCoord(coord : tuple) -> None

### method

- read() -> np.ndarray:
- get_id() -> str
- get_geo_coord_lat_lon() -> np.ndarray, np.ndarray
- get_geo_coord_lat_lon() -> np.ndarray
- get_xy_coord_vectors(lonSamplingRate: int = 277, latSamplingRate: int = - 277, enable_global : bool = False) -> np.ndarray
- transform_to_xy_coord(lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False) -> np.ndarray, np.ndarray, np.ndarray
- transform_to_geo_coord(): -> np.ndarray, np.ndarray, np.ndarray
- _covertCoordToXY(base, lonSamplingRate: int = 277, latSamplingRate: int = 277, enable_global = False) -> tuple

# Enum reference

## Enum `ResourceAttr` :

- UNIQUE_ID : resource unique id
- DB_ID : resource's id in database
- EXPIRE: exipired day
- LAST_UPDATE : the date of last update
- PATH: resource' path

## Enum `ResourceType` :

- MESH
- PCD