# Server Config
The default port of backend server is 9999, You can modofied this port in server.py line 13.
for example 
```
PORT = 6000
```
Currentlt backend deployed in localhost, that is 127.0.0.0. Please notice that all route is in the domain http://127.0.0.0:9999
# Route 
## /v1/download
### GET
Receive an id and a file type, read the corresponding file, and send it to the client. 
Example 
```
GET /v1/download?id=e14fa767-a876-4ee3-aea3-90509ae6fed7&type=mesh
```
The file will be cut into smaller files of 4096 each and sent and stitched together. If you use the browser to hit the link, The browser will take care of all the problems. Practically, no real response will be returned. The file's default name is test_download.ply. You would open this file at any 3d editing software you want. 
## POST /v1/api/region/mesh
### POST
Accept a JSON data, generate and return resources according to parameters.
Accepts two kinds of input
- polygon
- circle/center-point-square

In JSON Object, `type` define how you define the region, the key `data` is the passed paramarts  

**polygon Input**

Users can define multiple points to define any area as long as the three points are not collinear. At least two points are required, the coordinates of the two corners of a square region. 
> Note: Server currently assume user define a proper area, that is even if there are duplicate coordinates, at least two coordinates are not identical.

For this kind of input, you should define `type` as `polygon`. Each pair of latitude and longitude is define by a pair of key-value in JSON, for example{"latitude" : -33.005, "longitude" : 151.0056}. the data type of latitude and longitude is accept both string and any numeric data type. 
Therefore, The input should look like
```json
{
    "type" : "polygon",
    "data" : [
        {"latitude" : -33.005, "longitude" : 151.0056},
        {"latitude" : -33.021, "longitude" : 151.078},
        {"latitude" : "-33.037", "longitude" : "151.384"}
    ]
}
```
**circle/center-point-square**
Define a square area by defining a center and distance. The center can be any coordinate accepted by any backend, distance can be any distance as long as it's not too big due to disk-space consideration. 
> Because the current backend data only have coordinates between lat [-34, -33], lon [151, 152], please define the center in this range. But the distance can be any value, if the range exceeds the range of the backend, it will only return to blank in the exceeded part

For this kind of input you should define `type` as `circle`. The center of circle is a pair of latitude and longitude, which is a key-value pair. i.e.  {"latitude" : -33.005, "longitude" : 151.0056}. Similarly, latitude and longitude can be numbers or strings. `radius` define by a string or any number. `radius` also accpect a string and with some unit suck as km, m, yard, but the format of radius must be "{radius} {unit}". By default, radius will transfer to KM. 
Therefore, The input should look like
```json
{
    "type" : "circle",
    "data" : {
        "latitude" : -33.7, 
        "longitude" :  151.256,
        "radius" : 2
    }
}
```
**Response**
Response will contains 
- Download link `download`
- details
    - id of resource `id`
    - center coordinates on XYZ space `center` (unit m)
    - The minimum value of mesh at XYZ space `min-bound` (unit m)
    - The maximum value of mesh at XYZ space `max-bound` (unit m)
    - The geographic coordinate position corresponding to the coordinate origin of the XYZ coordinate system `geo-origin`

```json
{
  "download": "/v1/download?id=2cbbadfd-5289-44eb-bd28-babdffc9d68a&type=mesh",
  "details": {
    "id": "501203a0-6e3e-4925-836f-da5ab078df0c",
    "center": [
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
