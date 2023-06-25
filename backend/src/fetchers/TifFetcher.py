import math
from src.database.database import database
from src.fetchers.Exceptions import OutofServiceRange
from src.fetchers.FetchersConsts import TifAttr
class TifFetcher:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fetch_by_polygon(polygon, attr = TifAttr.UNIQUE_ID):
        lats = [row[0] for row in polygon]
        lons = [row[1] for row in polygon]
        min_bound = [math.floor(min(lats)), math.floor(min(lons))]
        max_bound = [math.ceil(max(lats)), math.ceil(max(lons))]
        # print(min_bound)
        # print(max_bound)
        
        result = database.fetchall(f"select {attr.value}, origin_lat, origin_lon from tifs where not (lat_end  < ? or  lat_begin > ?) and lon_begin >= ? and lon_end <= ?;",
                          [min_bound[0], max_bound[0], min_bound[1], max_bound[1]])
        uid = []
        base = []
        for each in result:
            if base == []:
                base = each[1:]
            
            if base[0] != each[1] or base[1] != each[2]:
                print("please check your mesh gereation, Database data is not in the same coordinate system.")
                print("Expected coordinate origin:", base, "Actual origin:", each[1:])
            else:
                uid.append(each[0])
        if uid == []:
            raise OutofServiceRange("Requested area is out of the service's working range.")
        # print(*base, uid)
        return base, uid

    @staticmethod
    def fetch_by_circle(center, radius, attr = TifAttr.UNIQUE_ID):
        est_arc = 1/111 * (radius / 1000)
        print("est arc:", est_arc)
        polygon = []
        for f in [-1, 1]:
            for l in [-1, 1]:
                polygon.append([center[0] + est_arc * f, center[1] + est_arc * l])
        return TifFetcher.fetch_by_polygon(polygon, attr)
    
    @staticmethod
    def fetch_all(attr = TifAttr.UNIQUE_ID):
        print(attr.value)
        print(f"select {attr.value}, origin_lat, origin_lon from tifs;")
        result = database.fetchall(f"select {attr.value}, origin_lat, origin_lon from tifs;")
        uid = []
        base = []
        for each in result:
            if base == []:
                base = each[1:]
            
            if base[0] != each[1] or base[1] != each[2]:
                print("please check your mesh gereation, Database data is not in the same coordinate system.")
                print("Expected coordinate origin:", base, "Actual origin:", each[1:])
            else:
                uid.append(each[0])
        return base, uid
    