# Urban AI Doc

# Documentation

Create an application that is commonly used in all areas of Sydney. This low-cost, convenient, and practical tool helps everyone access a city model quickly, facilitating further professional analysis such as heat analysis.

Using publicly available data, we developed a collection of tools that utilize AI and advanced data processing technology to analyze content specific to a given region. These tools enable the conversion of the analyzed content into a 3D model, which can then be displayed directly in a web browser. Furthermore, this toolset can be seamlessly adapted to other locations or implemented with higher-accuracy data sources, such as satellite imagery with higher resolution or improved clarity.
Overall Work Flow             |  Our Result
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%201.png)


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

- [Urban AI Server Reference ](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Urban%20AI%20Server%20Reference%20a55b3944407b41479a9b8a9faa6a619b.md)
- [API Reference](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/API%20Reference%208aab643b4ea7416288903ee193f7f7bb.md)

# Build Instructions

## Required packages:

- setup
    - pip
- server
    - flask >= 2.2.3
    - flask-restx >= 1.1.0
    - Flask-cors >= 3.0.10
- topography processing
    - open3d >= 0.13.0
    - numpy >= 1.24.2
    - geopy >= 2.3.0
    - geotiff >= 0.2.9
- Satellite detection
    - aiohttp==3.8.6
    - opencv-python==4.7.0.72
    - ultralytics==8.0.134
    - deepforest==1.0.0
    - sahi==0.11.14
    - torch==2.1.0
    - segmentation-models-pytorch==0.3.3
    - albumentations==1.3.1

## Install packages

From a run the following commands.

Installing a virtual environment depends library

```bash
python3 -m pip install --user virtualenv
```

Creating a virtual environment

```bash
python3 -m venv env
```

Activating the virtual environment

```bash
source env/bin/activate

```

Installing packages

```
pip3 install -r requirements.txt --quiet
```

Download TIFF files, you may be asked to enter 'YES' to continue. The download speed depends on the USGS server. You can configure the region you are going to use.

```
python downloader.py
```

Download the prediction models from the AWS Urban AI bucket and configure the model path in `src/config.py`. Then, run the server.

```
python server.py
```

# Tutorial

A brief tutorial of how the backend work and a brief summary of topography processing and satellite detection 

## Topography Tool

## Working flow

### Working flow diagram

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%202.png)

## Pre-processing Introduction

### Point Cloud Generation

This dataset has been fully pre-processed, converted from a TIF to a point cloud. A coordinate system transformation is also applied during this process, transitioning from geographic coordinates to local meter coordinates.

Considering the usage scenario for map projection, we did not use the common Mercator projection method. Instead, We used a modified version of the [Cassini Projection](https://en.wikipedia.org/wiki/Cassini_projection), where the base point is the center of our dataset instead of the Earth's polar point. We treat the latitude and longitude of the central point as the central meridian and latitude lines, respectively. Then, we calculate the distance from each point to these lines. The final projection is into the Cartesian coordinate system. Given the relatively small area of use (within NSW), map distortion is not a significant issue. However, if you plan to expand your data range to the country level in the future, you may need to reconsider the map projection. 

After the process, a PCD file will be saved to local storage. This file includes coordinates and their estimated normals.

### Mesh Generation

Mesh Generation is not fully pre-processed. There are scenarios where the program will process in real-time.  The unit of mesh is meters.  

Several algorithms exist for building a mesh, including cloud alpha, ball pivoting, and Poisson. We've chosen the Poisson algorithm with a depth of 9. It implements the Screened Poisson Reconstruction method proposed by Kazhdan and Hoppe in "Screened Poisson Surface Reconstruction," 2013. This function utilizes [Kazhdan's original implementation](https://github.com/mkazhdan/PoissonRecon).

**Pre-processing**

This is the most common scenario, where the majority of the requested region is pre-processed. To accomplish this, we create a relatively high-density mesh for each arc of the earth. Upon receiving a request, we crop the corresponding region. However, an error may occur in one particular case: if the region is too small and we can't find any triangular mesh surface within it. The output visualization will be as follows.
|  Output Visualization
:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%203.png)




**Real-time processing**

When a selection region is near the border of our pre-cached mesh, a gap may occur at the junction of the files due to the algorithm. This happens when several sub-mesh files are combined. In such cases, the file will be generated immediately. This method results in a higher mesh density, but also slightly increases the processing time. 
Real-time processing Cases             |  Output Visualization
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%204.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%205.png)

*Note: The selected region size is similar to the one above.*

## Server-side Introduction

This tutorial guides you through the essential preparations and steps to start the backend server. It covers the following topics:

- Starting the server
- Testing the server
- Optimization
- Databases
- Cache

### Start the server

This tutorial uses a single .tif as a cached dataset and assumes all request coordinates are within this region. We can run the server by:

```bash
python3 server.py
```

After running this command, you should find 'urbanAI.db' in the current working directory. Additionally, some resources will be generated in the data folder, such as 'pointcloud.pcd' and 'mesh.ply'. If this is your first time starting the server (i.e., a cold start), it may take a few seconds to prepare for server running. If not, this preparatory step is skipped.

If you have enough disk space, **DO NOT delete** 'urbanAI.db' unless you intend to redo the server preparation. Once everything is completed, you should see this type of message. 

### Test the server

**Manual Testing**

We recommend certain unit test tools for testing our backend, although we have not deployed any tests yet.

Unit Test Tools:

- requests >=2.28.2
- unittest

Currently, we use the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) (VSCode extension). We can send requests on our own and the responses will be displayed as shown.

```
# in request.rest

POST <http://127.0.0.1:9999/v1/api/region/mesh>
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

A full example is available in the `backend` folder, in a file called request.rest. This example should be quite straightforward. Here, "download" refers to the backend route used to download the resource. Other attributes in the responses detail the given region. The coordinates in the response typically represent XY plane coordinates, with the array representing [x, y, z].

During practical work, there may be an error thrown if a region is defined without any triangle mesh inside.

**Swagger**

We have developed a Swagger interface for testing our backend. You can access it using the backend IP address and port. The route for this tool is in the First namespace. Please feel free to use it.

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%206.png)

### Optimization

Through our code analysis, we found that the most time-consuming part of our process is reading pcd or ply files. Consequently, we implemented an option to compress these two file types and use less bitwidth data types with minor accuracy loss. Our tests show that this speeds up the reading time by 70% and significantly reduces disk space usage. The trade-off is slightly longer decompression time. By default, this optimization is not enabled. You may choose to optimize this step before running the server. 

```jsx
python optimizer.py
```

### Datasets

We currently use Sqlite3 as our database. Whenever we start the server and make any changes, the database is updated correspondingly. The database is synchronized, and the queries are somehow pipelined. Please note, there can only exist one database instance..

```
database1 = Database("urbanAI.db", tables)
database2 = Database("urbanAI2.db", tables)
database1 == database2
>>> True

```

The Database class is wrapped around the sqlite3 library, with the added advantage of providing multi-thread safe access to the database. When querying something, proceed as follows:.

```
database.start()
database.fetchall("select * from meshes;")
database.fetchall("select * from meshes where id = ?;", [id])
database.fetchone("select * from meshes where id = ?;", [id])
database.execute_in_worker("insert into tifs(xxxxxxxxx) values (? ...)", [params])

```

The database has a simple schema, which can be found in the Database class documentation.

### Cache

Each request to generate output is stored in memory. As we have a small user base, we haven't yet implemented a regular cache clean-up process. By default, the cache is cleared after every 80 mesh generations, and the corresponding mesh files are deleted. This means that you won't be able to download the resource after the clean-up. We recommend downloading the mesh as soon as it's generated and displayed.

If necessary, you can force the backend to clear the cache by sending a request with a specific key. However, we don't recommend doing this while a user is browsing the website as it could cause unpredictable behaviour. More information can be found in the backend management section.

The cache handles only the exact same input.

## Satellite Detection Tool

## Backend Management