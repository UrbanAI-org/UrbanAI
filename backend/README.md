# Documentation
The backend is a kind of tool for Mesh reconstruction based on the satatlite data, especially for the file type .tif. It also provides an API to exact and download the topography in given region.
# Quick Links
- [build-instructions](#build-instructions)
- [API and Classes Reference](#api-and-classes-reference)
- [tutorial](#tutorial)

# Supported platforms / languages
- Supported platforms
    - GNU/Linux
    - OS X
    - Linux
    - Windows (haven't test, it should support)
- Language
    - Python >= 3.8

# API and Classes Reference
- [Server Reference](./docs/RouteAPI.md)
- [Classes Reference](./docs/ClassesReference.md)

# Build Instructions
## Required packages:
- setup
    - pip
- server
    - flask >= 2.2.3
    - flask-restx >= 1.1.0
    - Flask-Cors >= 3.0.10
- topography processing
    - open3d >= 0.13.0
    - numpy >= 1.24.2
    - geopy >= 2.3.0
    - geotiff >= 0.2.9

## Install packages
From a run the following commands.
1. Installing a virtual environment depends library
```bash
python3 -m pip install --user virtualenv
```
2. Creating a virtual environment 
```bash
python3 -m venv env

```
3. Activating the virtual environment
```bash
source env/bin/activate
```
4. Installing packages
```
pip3 install -r requirements.txt
```
5. runing server
```
python server.py
```
# Tutorial
A brief tutorial of how the backend work and a brief summary of topography processing
## Introduction
This tutorial will walk you thorugh the main preperation and steps for starting the backend server. It will covers the following topics:
- Start the server
- Test the server
- Databases
- File structure
### Start the server
This tutorial uses one .tif as cahched dataset, and assumes all what reuquest's coordetate within this this dataset. We can runing the server by 
```bash
python3 server.py
```
After runing this command, you should have urbanAI.db in current working diroretry and also some resource generated in data folder such as pointcloud.pcd and mesh.ply. If it is your first time to start the server, i.e. cold start, This normally takes a few seconds to do some perperation for server running. Otherwise, the server would skip this step. 
If you have enough disk-space, do not delete the urbanAI.db unless you want to re-do server perperation.
Once everything is all done, this kind of message should print out.
```
* Serving Flask app 'server'
 * Debug mode: off
INFO - 2023-04-19 00:18:38,146 - _internal - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:9999
INFO - 2023-04-19 00:18:38,147 - _internal - Press CTRL+C to quit
```
### Test the server
We do recommand some unit test tools to test our backend, but we are not deploy any test yet. 

Unit Test Tools
- requests >=2.28.2
- unittest

We currently used.
- [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) (VSCode extension)
We can send request by our own then response will come uo as follows shown:
```text
# in request.rest

POST http://127.0.0.1:9999/v1/api/region/mesh 
content-type: application/json

{
    "type" : "polygon",
    "data" : [
        {"latitude" : -33.005, "longitude" : 151.0056},
        {"latitude" : -33.01, "longitude" : 151.01}
    ]
}


# response poped up
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.8.10
Date: Tue, 18 Apr 2023 13:41:14 GMT
Content-Type: application/json
Content-Length: 405
Access-Control-Allow-Origin: *
Connection: close

{
  "download": "/v1/download?id=2cbbadfd-5289-44eb-bd28-babdffc9d68a&type=mesh",
  "mesh": "mesh",
  "details": {
    "id": "501203a0-6e3e-4925-836f-da5ab078df0c",
    "center": [
      -22183.036500283404,
      -22673.095447618794,
      104.541015625
    ],
    "min-bound": [
      -24183.036500283404,
      -24673.095447618794,
      -1.984375
    ],
    "max-bound": [
      -20183.036500283404,
      -20673.095447618794,
      211.06640625
    ],
    "geo-origin": [
      -33.50000000000001,
      151.5
    ]
  }
}


```
The full example is availble in `backend` folder called request.rest.
For the most part, this example should be pretty straightforward. Note "download" refers the route in backend to downlond the resource. and other attribute in responses is the details of given region. the coordinates in response generally represent in XY plance coordinates. The representation of given array is [x, y, z].

There would be a possible error that could thrown in practial work. If we defined a region that there isn't ant trangle mesh is inside. 

### Datasets
We currently use Sqlite3 as our database. Once we start the server and make any meshes, the database is always update correspobdingly. The database is synchronized, the qury for the database is piplined somehow. Notice, I have limate only exist one database instance. 
```py
database1 = Database("urbanAI.db", tables)
database2 = Database("urbanAI2.db", tables)
database1 == database2
>>> True
```
Class Database is warped around the sqlite3 library, the only difference is that Database is provide multi-thread safe access for the database. Each time when qury something, doing it like this. 
```py
database.start()
database.fetchall("select * from meshes;")
database.fetchall("select * from meshes where id = ?;", [id])
database.fetchone("select * from meshes where id = ?;", [id])
database.execute_in_worker("insert into tifs(xxxxxxxxx) values (? ...)", [params])
```
Database have a simple schema, you could find it the Database class documation.
## File structure
- backend
    - server.py
    - urbanAI.db
    - src
        - database
            - database.py
                - class `Database`
            - singletonMeta.py
                - class `SingletonMeta`
        - fetchers
            - regionDataFetcher.py
                - class `RegionDataFetcher`
            - resourceFetcher.py
                - class `ResourceFetcher` (ABC)
                - class `MeshResourceFetcher`
                - class `PcdResourceFetcher`
            - FetchersConsts.py
                - Enum `ResourceAttr` : UNIQUE_ID, DB_ID, EXPIRE, LAST_UPDATE, PATH
                - Enum `ResourceType` : MESH, PCD
            - TifRegionFetcher.py
                - class `TifRegionFetcher`
        - loaders
            - tifLoader.py
                - class `TifLoader`
            - utils.py
    - data
        - meshes
            - xxx.ply
        - pcds
            - xxx.pcd
        - xxx.tif

If you want to change the cached tif file, please put tif file in the `data` folder, and delete the database and put path of tif into the server.py line 97.
```
loader = TifLoader("data/any.tif")

```
