import math
from src.database.database import database
from src.fetchers.Exceptions import OutofServiceRange
from src.fetchers.FetchersConsts import TifAttr
class TifFetcher:
    def __init__(self) -> None:
        pass

    @staticmethod
    def fetch_by_polygon(polygon, attr=TifAttr.UNIQUE_ID):
        """
        Fetches data from the database based on a given polygon.

        Args:
            polygon (list): List of coordinates representing the polygon.
            attr (TifAttr, optional): Attribute to fetch from the database. Defaults to TifAttr.UNIQUE_ID.

        Returns:
            tuple: A tuple containing the base coordinates and a list of unique IDs.

        Raises:
            OutofServiceRange: If the requested area is out of the service's working range.
        """
        lats = [row[0] for row in polygon]
        lons = [row[1] for row in polygon]
        min_bound = [math.floor(min(lats)), math.floor(min(lons))]
        max_bound = [math.ceil(max(lats)), math.ceil(max(lons))]
        
        result = database.fetchall(f"select {attr.value}, origin_lat, origin_lon from tifs where not (lat_end  < ? or  lat_begin > ?) and lon_begin >= ? and lon_end <= ?;",
                          [min_bound[0], max_bound[0], min_bound[1], max_bound[1]])
        uid = []
        base = []
        for each in result:
            if base == []:
                base = each[1:]
            
            if base[0] != each[1] or base[1] != each[2]:
                print("please check your mesh generation, Database data is not in the same coordinate system.")
                print("Expected coordinate origin:", base, "Actual origin:", each[1:])
            else:
                uid.append(each[0])
        if uid == []:
            raise OutofServiceRange("Requested area is out of the service's working range.")
        
        return base, uid

    @staticmethod
    def fetch_by_circle(center, radius, attr = TifAttr.UNIQUE_ID):
        """
        Fetches data from a TIF file based on a circular area.

        Parameters:
        - center: The center coordinates of the circle (latitude, longitude).
        - radius: The radius of the circle in meters.
        - attr: The attribute to fetch from the TIF file (default: TifAttr.UNIQUE_ID).

        Returns:
        - The fetched data.

        """
        est_arc = 1/111 * (radius / 1000)
        print("est arc:", est_arc)
        polygon = []
        for f in [-1, 1]:
            for l in [-1, 1]:
                polygon.append([center[0] + est_arc * f, center[1] + est_arc * l])
        return TifFetcher.fetch_by_polygon(polygon, attr)
    
    @staticmethod
    def fetch_all(attr = TifAttr.UNIQUE_ID):
        """
        Fetches all data from the 'tifs' table in the database.

        Args:
            attr (TifAttr): The attribute to select from the table. Defaults to TifAttr.UNIQUE_ID.

        Returns:
            tuple: A tuple containing the base coordinate and a list of unique IDs.
        """
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
    