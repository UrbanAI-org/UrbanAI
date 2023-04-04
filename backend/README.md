**All backends use RESTFUL style**
# Routes Overview
- /v1/query/chunks
    - GET : get a list of select of area chunks
    - POST: create a area chunks
- /v1/query/chunk
    - GET: get information about this chunk

- /v1/resource
    - GET: get resource from backend
    - POST: let the backend generate corresponding resources
- /v1/download
    - GET: download corresponding resources
# Start the server
```bash
cd backend
python server.py
```
If it is a cold start, it will take a while.

# How to use
1. First send a POST request to create a chunk
``` 
POST /v1/query/chunks
Request:
{
    "type" : "polygon",
    "data" : {
        "polygon" : [
            (-33.005, 151.0056),
            (-33.021, 151.078),
            (-33.037, 151.384),
        ]
    },
}

Response:
{
    'id' : chunk_id,
    'herf': f"/v1/query/chunk?id={chunk_id}", 
    
}
```
2. According to the link returned in the first step, check the chunk information
```
GET /v1/query/chunk?id={id}

Response :
{
    'id' : chunk_id,
    'center' : [-3500, -3500, 0],
    'min-bound' : [-5000, -5000, -1000],
    'max-bound' : [-3000, -3000, 1000],
    'last-update' : "2023-04-04 12:00:00",
    'geo-origin' : [-33.5, 151.5],
    'parent': 's34_e151_1arc_v3.tif',
    'status' : {
        'Mesh' : {
            "exist" : True,
            'id' : mesh_resource_id,
            'herf': f"/v1/resource?id={mesh_resource_id}", 
            'download' : f"/v1/download/{mesh_resource_id}",
            'expired' : 3  # days
        },
        'Pcd' : {
            "exist" : False,
            'herf' : f"/v1/resource",
            'args' : {
                'chunk-id' : xxxxx,
                'type' : 'pcd'
            }
        },
    },
}
```
There are two cases at this time, 
    - if the file has not been generated, the response will contain links and parameters to the generated file. You only need to send a POST requests to returned link with args to generate the corresponding file
    - If the file has already generated, the responses will contains links to open download stream or transfer the file in HTTP response.
    
3. Assuming we don't have any files present, we send a POST to /v1/resource with args, if we take above response as an example.
```
POST /v1/resource
Request:
{
    'chunk-id' : xxxxx,
    'type' : xxxx
}

Response:
{
    'id' : xxxxx,
    'herf': f"/v1/resource?id={xxxx}&type={pcd}",
    'expired' : 3
}  

```
Returns a link to transfer the file in HTTP response and other related infomation.


# Details
## /v1/query/chunks
### GET
```
GET /v1/query/chunks

Response: 
{
    "chunks" : [
        {
            "id" : chunk_id,
            'herf': f"/v1/query/chunk?id={chunk_id}"
        }
    ]
}

```
**Return All existing chunks ** 


### POST

```
POST /v1/query/chunks
Request:
{
    "type" : "polygon",
    "data" : {
        "polygon" : [
            (-33.005, 151.0056),
            (-33.021, 151.078),
            (-33.037, 151.384),
        ]
    },
}
OR
{
    "type" : "circle",
    "data" : {
        "center" : [-33.5, 151.5],
        "radius" : "2 km" # more option could be 200m, 2 mile....
    },
}
OR 
MORE IF YOU WANT

Response:
{
    'id' : chunk_id,
    'herf': f"/v1/query/chunk?id={chunk_id}", 
    
}

```
Receive the corresponding search parameters and create new corresponding chunks


## /v1/query/chunk
### GET
```
GET /v1/query/chunk?id={id}

Response :
{
    'id' : chunk_id,
    'center' : [-3500, -3500, 0],
    'min-bound' : [-5000, -5000, -1000],
    'max-bound' : [-3000, -3000, 1000],
    'last-update' : "2023-04-04 12:00:00",
    'geo-origin' : [-33.5, 151.5],
    'parent': 's34_e151_1arc_v3.tif',
    'status' : {
        'Mesh' : {
            "exist" : True,
            'id' : mesh_resource_id,
            'herf': f"/v1/resource?id={mesh_resource_id}", 
            'download' : f"/v1/download/{mesh_resource_id}",
            'expired' : 3  # days
        },
        'Pcd' : {
            "exist" : False,
            'herf' : f"/v1/resource",
            'args' : some_args
        },
    },
}

```
Receive the ID and return the corresponding information

## /v1/resource
### GET: get resource from backend
```
GET /v1/resource?id={id}

Response:
.ply file directly

```
send ply file

### POST: let the backend generate corresponding resources
```
POST /v1/resource
Request:
{
    args: {args}
    # FOLLOW BY `GET /v1/query/chunk` Returns.
}

```
If there is no resource file, according to the parameters sent by the backend before, send it to the backend to generate the required resources. see [details](#v1querychunk)


## /v1/download
### GET
```
GET /v1/download?id={id}

Response:
.ply file directly

```
download ply file as a attachement
