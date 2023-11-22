from io import BufferedReader
# from src.database.database import database
from src.database.database import database
from src.fetchers.FetchersConsts import ResourceAttr, ResourceType
from datetime import datetime
import os
class ResourceFetcher:
    def __init__(self, domain, database) -> None:
        """
        Initializes a ResourceFetcher object.

        Args:
            domain (ResourceType): The type of resource domain.
            database: The database to fetch resources from. Haven't implemented this yet.

        Returns:
            None
        """
        assert type(domain) is ResourceType
        self.domain = domain.value
    
    def get_pth(self, by : ResourceAttr, value):
        """
        Get the path of a resource based on the specified attribute and value.

        Args:
            by (ResourceAttr): The attribute to search by.
            value: The value to search for.

        Returns:
            str: The path of the resource.
        """
        return self._get_attr_by_attr(ResourceAttr.PATH, by, value)
    
    def get_content(self, by: ResourceAttr, value) -> BufferedReader:
        """
        Retrieves the content of a resource based on the specified attribute and value.

        Args:
            by (ResourceAttr): The attribute to search by.
            value: The value to search for.

        Returns:
            BufferedReader: The content of the resource as a buffered reader.

        Raises:
            FileNotFoundError: If the file is not found.
        """
        pth = self.get_pth(by, value)
        if pth is None:
            raise FileNotFoundError("file does not found by", by.name, ":", value)
        file = open(pth, "rb")
        return file
    
    def get_uid(self, by, value):
        """
        Get the unique identifier (UID) of a resource based on the specified attribute.

        Args:
            by (str): The attribute to search by.
            value: The value of the attribute to search for.

        Returns:
            The unique identifier (UID) of the resource.

        """
        return self._get_attr_by_attr(ResourceAttr.UNIQUE_ID, by, value)

    def get_db_id(self, by: ResourceAttr, value):
        """
        Retrieves the database ID of a resource based on the specified attribute.

        Args:
            by (ResourceAttr): The attribute to search by.
            value: The value of the attribute to search for.

        Returns:
            The database ID of the resource.

        """
        return self._get_attr_by_attr(ResourceAttr.DB_ID, by, value)

    def _get_attr_by_attr(self, result: ResourceAttr, by: ResourceAttr, value):
        """
        Retrieves the attribute value of a resource based on another attribute value.

        Args:
            result (ResourceAttr): The attribute to retrieve from the resource.
            by (ResourceAttr): The attribute to use as a filter.
            value: The value of the filter attribute.

        Returns:
            The attribute value of the resource that matches the filter attribute value.
            If no matching resource is found, returns None.
        """
        assert type(by) is ResourceAttr
        assert type(result) is ResourceAttr
        if value is None:
            return None
        if type(value) is list:
            return [self._get_attr_by_attr(result, by, each) for each in value]
                
        qry = f"""
        select {result.value} from {self.domain} where {by.value} = ?;
        """
        data = database.fetchone(qry, [value])
        if data is None:
            return None
        else:
            return data[0]
    def write_to_database(self, uid, path, expired=3):
        """
        Writes the resource information to the database.

        Args:
            uid (str): The unique identifier of the resource.
            path (str): The path of the resource.
            expired (int, optional): The expiration time of the resource in days. Defaults to 3.

        Returns:
            int: The ID of the resource in the database.
        """
        qry = f"""
            insert or replace into {self.domain}(uid, expired, last_update, pth) 
            values (?,?,?,?);
            """
        database.execute_in_worker(qry, [uid, expired, datetime.now().timestamp(), path])
        id = self.get_db_id(ResourceAttr.UNIQUE_ID, uid)

        return id
    
    
    
class MeshResourceFetcher(ResourceFetcher):
    """
    A class for fetching MESH resources.

    Inherits from the ResourceFetcher class.
    """

    def __init__(self) -> None:
        super().__init__(ResourceType.MESH)
    
    


class PcdResourceFetcher(ResourceFetcher):
    """
    A class for fetching PCD resources.

    Inherits from the ResourceFetcher class.
    """

    def __init__(self) -> None:
        super().__init__(ResourceType.PCD)
    

class TreeModelResourceFetcher():
    """
    A class that fetches tree model resources.

    Attributes:
    - root_path (str): The root path where the tree model resources are stored.

    Methods:
    - get_pth(by: ResourceAttr, value): Returns the path of the tree model resource based on the specified attribute and value.
    - get_uid(by: ResourceAttr, value): Returns the unique ID of the tree model resource based on the specified attribute and value.
    - get_db_id(by: ResourceAttr, value): Returns the database ID of the tree model resource based on the specified attribute and value.
    - write_to_database(uid, path, expired): Writes the tree model resource to the database with the specified unique ID, path, and expiration time.
    """

    def __init__(self, root_path = "data/treemodels/") -> None:
        self.root_path = root_path

    def get_pth(self, by : ResourceAttr, value):
        if by.name == "UNIQUE_ID" and os.path.exists(f"{self.root_path}/{value}.obj"):
            return f"{self.root_path}/{value}.obj"
        else:
            return None
    
    def get_uid(self, by : ResourceAttr, value):
        return value
    
    def get_db_id(self, by: ResourceAttr, value):
        return None
    
    def write_to_database(self, uid, path, expired = 3):
        pass
    
# class RoadModelResourceFetcher():
#     def __init__(self, domain, database) -> None:
#         super().__init__(domain, database)