import aiohttp
import asyncio
import numpy as np
import cv2
from src.fetchers.Exceptions import BBoxIsLarge
from src.config import GOOGLE_STATICMAP_URL, GOOGLE_STATICMAP_TOKEN
import geopy.distance
# fetch one image from google static map api
async def fetch_one(session, lat, lng, zoom = 19, maptype = 'satellite'):
    params={
        'size' : '600x600',
        'format' : 'PNG',
        'maptype' : maptype,
        'key' : GOOGLE_STATICMAP_TOKEN,
        'center' : f"{lat}, {lng}",
        'zoom' : zoom
    }
    async with session.get(GOOGLE_STATICMAP_URL, params = params) as response:
        if response.status == 200:
            arr = np.asarray(bytearray(await response.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            cropped_image = image[0:image.shape[0]-20, 60:image.shape[1]-60]
            return cropped_image
        else:
            image = np.zeros((580, 480, 3), dtype=np.uint8)
            image.fill(255)
            return  image


# fetch one row of images from google static map api
async def fetch_one_row(session, center_lat, west, lng_tiles, lng_step, zoom = 19, maptype = 'satellite' ):
    tasks = []
    for i in range(lng_tiles):
        center_lng = west + i * lng_step + lng_step / 2
        tasks.append(fetch_one(session, center_lat, center_lng, zoom, maptype))
    row_tiles = await asyncio.gather(*tasks)
    row_image = np.zeros((580, 480 * lng_tiles, 3), dtype=np.uint8)
    x_offset = 0
    for img in row_tiles:
        h, w, _ = img.shape
        row_image[0:h, x_offset:x_offset+w] = img
        x_offset += w
    return row_image

# fetch all images from google static map api
async def fetch_all(south, west, lat_tiles, lat_step, lng_tiles, lng_step, zoom = 19, maptype = 'satellite'):
    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector = connector ) as session:
        tasks = []
        for i in range(lat_tiles):
            center_lat = south + i * lat_step + lat_step / 2
            tasks.append(fetch_one_row(session, center_lat, west, lng_tiles, lng_step, zoom, maptype))
        rows = await asyncio.gather(*tasks)
        final_image = np.zeros((580 * lat_tiles, 480 * lng_tiles, 3), dtype=np.uint8)
        y_offset = 0
        for img in reversed(rows):
            h, w, _ = img.shape
            final_image[y_offset:y_offset+h, 0:w] = img
            y_offset += h
        return final_image     

def _align_rectangle(coords, lat_step, lng_step):
    aligned_south = round(coords['south'] / lat_step) * lat_step
    aligned_west = round(coords['west'] / lng_step) * lng_step
    aligned_north = aligned_south + ((round((coords['north'] - coords['south']) / lat_step) + 1) * lat_step)
    aligned_east = aligned_west + ((round((coords['east'] - coords['west']) / lng_step) + 1) * lng_step)
    
    return {
        'south': aligned_south,
        'west': aligned_west,
        'north': aligned_north,
        'east': aligned_east
    }

def fetch_satellite_image(coords, maptype = 'satellite') -> np.ndarray:
    # Google Maps Static API URL
    zoom = "19"
    
    # Calculate latitude and longitude steps
    METERS_PER_PIXEL_AT_ZOOM_19 = 0.2986
    METERS_PER_DEGREE_LATITUDE = 111000  # 111 km in meters
    SIZE_IN_METERS = 600 * METERS_PER_PIXEL_AT_ZOOM_19
    lat_step = (SIZE_IN_METERS / METERS_PER_DEGREE_LATITUDE) * 0.8
    lng_step = lat_step
    
    # Align the coordinates with the step size
    aligned_coords = _align_rectangle(coords, lat_step, lng_step)
    
    # Divide the selected region into tiles
    south, west, north, east = aligned_coords.values()
    lat_tiles = max(1, int((north - south) / lat_step))
    lng_tiles = max(1, int((east - west) / lng_step))
    print("lat_tiles", lat_tiles)
    print("lng_tiles", lng_tiles)
    final_bgr_image = asyncio.run(fetch_all(south, west, lat_tiles, lat_step, lng_tiles, lng_step, zoom, maptype))
    cv2.imwrite("stitched_image.png", final_bgr_image)
    return final_bgr_image
    # Save the final stitched image


class StatelliteFetcher:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fetch_by_polygon(polygon, maptype = 'satellite'):
        lats = [row[0] for row in polygon]
        lngs = [row[1] for row in polygon]
        coords = {"south":min(lats),
        "west":min(lngs),
        "north":max(lats),
        "east":max(lngs)}
        width = geopy.distance.distance((coords['north'], coords['east'],), ( coords['north'], coords['west'])).km
        height = geopy.distance.distance((coords['north'], coords['east'],), ( coords['south'], coords['east'])).km
        if width > 1 or height > 1:
            raise BBoxIsLarge("Given region is too large to process")
        return fetch_satellite_image(coords, maptype)
    
   