# Urban AI Documentation

Create an application that is commonly used in all areas of Sydney. This low-cost, convenient, and practical tool helps everyone access a city model quickly, facilitating further professional analysis such as heat analysis.

Using publicly available data, we developed a collection of tools that utilize AI and advanced data processing technology to analyze content specific to a given region. These tools enable the conversion of the analyzed content into a 3D model, which can then be displayed directly in a web browser. Furthermore, this toolset can be seamlessly adapted to other locations or implemented with higher-accuracy data sources, such as satellite imagery with higher resolution or improved clarity.
Overall Work Flow             |  Our Result
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%201.png)
# Report bugs or advices
Please fill this [form](https://docs.google.com/forms/d/e/1FAIpQLSeDCRgAMDRd8n3Bz68ILfMUSrYcpRR4zKRpurCH_jJVqunqXw/viewform)

# Table of Content

- [Build instructions](#build-instructions)
- [API and Classes Reference](#api-and-classes-reference)
- [Tutorial](#tutorial)
  - [Topography Tool](#topography-tool)
    - [Working flow](#working-flow)
    - [Pre-processing Introduction](#pre-processing-introduction)
    - [Server-side Introduction](#server-side-introduction)
  - [Satellite Detection Tool](#satellite-detection-tool)
    - [Working Flow](#working-flow-1)
    - [Trees Detection](#trees-detection)
    - [Tree Clustering](#tree-clustering)
    - [Roofs Segmentation](#roofs-segmentation)
    - [Roads Segmentation](#roads-segmentation)
  - [Backend Management](#backend-management)
    - [Logging](#logging)
    - [Clean Logs and Resources](#clean-logs-and-resources)
    - [Swagger](#swagger)

# Supported platforms / languages

- Supported platforms
    - GNU/Linux
    - OS X
    - Linux
    - Windows (haven't test, it should support)
- Language
    - Python >= 3.8

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
### Frontend 
run the frontend.
```bash
cd frontend
npm start
```
Note that you may be required to build the project in which case run:

```
npm run build
```

### Backend
``` bash
cd backend
```
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

### Download Tifs from USGS

The United States Geological Survey (USGS) offers a [Machine-to-Machine API](https://m2m.cr.usgs.gov/api/docs/json/) for users to request resources. This API allows automated systems to interact and exchange data with the USGS database, facilitating seamless data retrieval. To use this service, users must first sign into the USGS platform. Upon successful login, a form can be submitted to obtain a free access token. This token serves as a key to authenticate and authorize the user's requests to the USGS API. It's a simple and efficient way to access a vast array of resources provided by USGS. Obtaining an application token using a student email would be relatively easy.
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%200.png)

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
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%204.png)




**Real-time processing**

When a selection region is near the border of our pre-cached mesh, a gap may occur at the junction of the files due to the algorithm. This happens when several sub-mesh files are combined. In such cases, the file will be generated immediately. This method results in a higher mesh density, but also slightly increases the processing time. 
Real-time processing Cases             |  Output Visualization
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%205.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%206.png)

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

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2042.png)

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

The Satellite Detection Tool uses Google's satellite photos to find common things like trees, buildings, and roads. To do this, we've trained AI models. These models can do two important things: object segmentation and object detection. Object segmentation means finding the exact pixels in a picture that make up an object. Object detection means finding where objects are in a picture.
Statellite Image             |   Building Segementation
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%208.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%209.png)
**Road segmentation**             |   **Tree Detection**
![roads.png](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/roads.png)        |  ![trees.png](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/trees.png)

### Working flow

![x](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/workflow.png)

### Trees Detection

This task uses the [deepforest model](https://deepforest.readthedocs.io/en/latest/) primarily for detection, though it can also be used for classification. Since the pre-trained model isn't quite suited to our target area, we fine-tune it using a small [labeled dataset](https://universe.roboflow.com/unsw-urbanai/tree-detection-in-sydney). The challenge lies in distinguishing between a tree, grass, or a green roof, and identifying when two or more trees are connected. You can find training notebook at backend folder.

The model performs well for the first challenge, but the second one still requires more effort and has room for improvement. Overall, it appears to effectively identify most of the trees in the image.
Distinguishing between a tree, grass      |   Identifying when two or more trees 
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2010.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2011.png)





It can also be used for a tile image, retaining good performance even over a large area.

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2012.png)

### Tree Clustering

After the relatively accurate prediction of trees, each tree is isolated and segmented, giving us a substantial dataset composed of various types of trees. This process of segmentation is vital for our subsequent analyses and processes, and it allows us to individually study each tree in the dataset.

However, a significant challenge we face is the quality of the satellite images. The images often depict trees as blurry, making it difficult for us to distinguish and cluster them accurately. Hence, we have explored two different approaches. 

**Approach One: The One that server used**

This method involves extracting the RGB channel information from each image as factors. After performing PCA dimensionality reduction, the K-Means Cluster is used. This approach categorizes trees into several groups based on their colour, considering that different types of trees have different leaf colours.

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2013.png)

We found the best K through this graph, that is, k=7, which divides all trees into seven different types.

After cluster, we observe those trees, we conclude the features for each types of tree

|  | Class 1 | Class 2 | Class 3 | Class 4 | Class 5 | Class 6 | Class7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sample Image | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2014.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2015.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2016.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2017.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2018.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2019.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2020.png) |
| Colour | Very dark |  | Slightly greener than the Class 1 | dark, and yellow-green | The leaves are relatively more yellow-green |  | Green, and relative yellow-green like |
| Leaf density | highest density | Not very dense | Not very dense | Not very dense, Some is sparse | Not very dense | Not very dense, Some is sparse | Not very dense, or dead tree |
| Shape | ~ | Most have relatively round crowns | Irregular shape crowns and round crowns |  |  | Most have relatively round crowns | Most have relatively round crowns |
| Other | Many of the same trees often appear together | in most cases there is only one tree |  | The crown of the tree is very large, or many trees appear together | The size of the tree is relatively small | The leaves of smaller trees are generally sparse, while the leaves of smaller trees are generally not very dense. | Many in this class are not trees, some are dead wood, and the rest are relatively small trees. |

**Approach Two:** 

Our process begins by encoding the data using a neural network, specifically VGG16. This transforms the image content into a vectorized format, allowing the network to effectively comprehend it. Once the image data is vectorized, we proceed to PCA dimensionality reduction. Following this, we use the K-Means Clustering algorithm to distinguish between different types of trees in the image. KNN works by examining and comparing tree characteristics, enabling us to group them into distinct categories.

This method roughly categorizes trees according to their shape (width and height) and colour. But the difference from the previous method is not particularly big. Since this method will consume more performance, this method has not been studied in depth.

Roughly divided into fourteen categories
|  | Class 1 | Class 2 | Class 3 | Class 4 | Class 5 | Class 6 | Class 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sample Image | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2021.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2022.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2023.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2024.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2025.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2026.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2028.png) |
|   | **Class 8** | **Class 9** | **Class 10** | **Class 11** | **Class 12** | **Class 13** |**Class 14** |
| Sample Image | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2029.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2030.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2031.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2032.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2025.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2033.png) | ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2034.png) |


### Roofs Segmentation

In this task, we use the [YOLOv8s-seg](https://docs.ultralytics.com/tasks/segment/) model for roof segmentation. This model has proven effective in distinguishing roofs. We began by basing our work on this model and initially trained it using a dataset without augmentation. After this initial training, we fine-tuned the model to increase its robustness. We conducted several training iterations using different augmentations. Notably, our model's capabilities extend beyond identifying ordinary house roofs - it has also shown considerable proficiency in recognizing factory roofs.

Factory Roofs      |   Building Roofs 
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2035.png)  |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2036.png)


It can also be used for a tile image, retaining good performance even over a large area.

Segmentation with border      |   Segmentation Mask 
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2037.png) |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%209.png)





*Note: As the process involves large-scale mask splicing, there might be a risk of insufficient memory. However, we have addressed this issue. This process may result in the same house being stitched together from multiple separate masks. Regardless, this will not affect the actual mask.*

You can find our dataset [here](https://universe.roboflow.com/unsw-urbanai/roof-segment) and the training notebook at backend folder. Please note that the model used on the server differs from the one deployed in the Roboflow, with the server model being more accurate.

### Roads Segmentation

In this task, we leverage Semantic Segmentation employing [DeepLabV3+](https://arxiv.org/abs/1802.02611) within the PyTorch framework. DeepLabV3+ has demonstrated remarkable capabilities in image segmentation. For a comprehensive understanding of its workflow and practical examples, refer to this informative [essay](https://learnopencv.com/deeplabv3-ultimate-guide/#DeepLabv3+-Paper-Experiments).

Our approach involves training the model with satellite images. Post-training, we evaluate the model using the Intersection over Union (IoU) score to ascertain its segmentation accuracy. The achieved IoU score of approximately 0.94 indicates the model's proficiency in accurately segmenting roads.

Presented below is an illustrative example of the segmentation result:

To generate a predictive graph, we utilize the mask image obtained during the segmentation process.

 Image      |   Road Masks 
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2038.png) |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2039.png)

It can also be used for a tile image, retaining good performance even over a large area.

Large area image      |   Segmentation mask
:-------------------------:|:-------------------------:
![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%208.png) |  ![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2040.png)
The model was trained using data from Google's road map, and we created the masks for the training from roadmap, and training process is also in backend folder.


*Note: The road appears discontinuous due to trees obscuring some narrow paths. Also, the model does not segment the train rail.*

## Backend Management

### Logging

The backend system generates and maintains two distinct types of logs, each serving a specific purpose. The first type is the error log, named `server.log`. This log is designed to keep track of any errors that occur within the system. It records the occurrence of errors along with their corresponding messages, providing a detailed traceback.

The second type of log is referred to as `users.log`. This log is dedicated to monitoring user activity. It systematically records the IP address of each user, the time of their last access to the system, and the dates when these accesses occurred. 

### Clean Logs and Resources

The backend system of our application requires a particular Key to execute associated commands. This Key is not a fixed value but is instead generated randomly whenever the server permits its generation. It's crucial to note this Key when you start the server, as it will be required for future operations on the backend.

In case you forget this Key. There are two methods by which you can retrieve it. The first method involves providing a password. Once the correct password is given, the system will reveal the Key. The second method involves sending a 'GET' request to the corresponding route that resides under the same IP as the server. Through either of these methods, you can retrieve the Key and continue managing the backend operations successfully.

### Swagger

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2041.png)

Swagger enables the description of API structures in a machine-readable format. In this project, there are three namespaces. The default namespace primarily serves management backend and related routes, while the other two tools each have their own independent namespaces.

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2042.png)

![Untitled](Urban%20AI%20Doc%2070c57da3d24c45f5ac043dfda1086582/Untitled%2043.png)

Each route possesses default values for testing. These can be edited to test the backend. To edit the payload, simply click the 'try it out' button located in the upper right corner.

# Possible Error Thrown
You may have the error like this,
```
Error: error:0308010C:digital envelope routines::unsupported
    at new Hash (node:internal/crypto/hash:71:19)
    at Object.createHash (node:crypto:140:10)
    at module.exports (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/util/createHash.js:90:53)
    at NormalModule._initBuildHash (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:386:16)
    at handleParseError (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:434:10)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:466:5
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:327:12
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:373:3
    at iterateNormalLoaders (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:214:10)
    at iterateNormalLoaders (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:221:10)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:236:3
    at runSyncOrAsync (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:130:11)
    at iterateNormalLoaders (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:232:2)
    at Array.<anonymous> (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:205:4)
    at Storage.finished (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/enhanced-resolve/lib/CachedInputFileSystem.js:55:16)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/enhanced-resolve/lib/CachedInputFileSystem.js:91:9
/home/shilong/urbanAI/UrbanAI/frontend/node_modules/react-scripts/scripts/start.js:19
  throw err;
  ^

Error: error:0308010C:digital envelope routines::unsupported
    at new Hash (node:internal/crypto/hash:71:19)
    at Object.createHash (node:crypto:140:10)
    at module.exports (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/util/createHash.js:90:53)
    at NormalModule._initBuildHash (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:386:16)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:418:10
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/webpack/lib/NormalModule.js:293:13
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:367:11
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:233:18
    at context.callback (/home/shilong/urbanAI/UrbanAI/frontend/node_modules/loader-runner/lib/LoaderRunner.js:111:13)
    at /home/shilong/urbanAI/UrbanAI/frontend/node_modules/babel-loader/lib/index.js:51:103 {
  opensslErrorStack: [ 'error:03000086:digital envelope routines::initialization error' ],
  library: 'digital envelope routines',
  reason: 'unsupported',
  code: 'ERR_OSSL_EVP_UNSUPPORTED'
}

```
You can use this command to resolve this problem. Because this problem is due to security issues. 
```bash
export NODE_OPTIONS=--openssl-legacy-provider
```
