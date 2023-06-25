from io import BufferedReader
from src.database.database import database
from src.fetchers.FetchersConsts import ResourceAttr, ResourceType
from datetime import datetime
class ResourceFetcher:
    def __init__(self, domain) -> None:
        assert type(domain) is ResourceType
        self.domain = domain.value
    
    def get_pth(self, by : ResourceAttr, value):
        return self._get_attr_by_attr(ResourceAttr.PATH, by, value)
    
    def get_content(self, by: ResourceAttr, value) -> BufferedReader:
        pth = self.get_pth(by, value)
        if pth is None:
            raise FileNotFoundError("file does not found by", by.name, ":", value)
        file = open(pth, "rb")
        return file
    def get_uid(self, by, value):
        return self._get_attr_by_attr(ResourceAttr.UNIQUE_ID, by, value)

    def get_db_id(self, by: ResourceAttr, value):
        return self._get_attr_by_attr(ResourceAttr.DB_ID, by, value)

    def _get_attr_by_attr(self, result: ResourceAttr, by: ResourceAttr, value):
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
    def write_to_database(self, uid, path, expired = 3):
        qry = f"""
            insert or replace into {self.domain}(uid, expired, last_update, pth) 
            values (?,?,?,?);
            """
        database.execute_in_worker(qry, [uid, expired, datetime.now().timestamp(), path])
        id = self.get_db_id(ResourceAttr.UNIQUE_ID, uid)

        return id
    
    
    
class MeshResourceFetcher(ResourceFetcher):
    def __init__(self) -> None:
        super().__init__(ResourceType.MESH)
    
    


class PcdResourceFetcher(ResourceFetcher):
    def __init__(self) -> None:
        super().__init__(ResourceType.PCD)
    
    # def get_pth(self, by : ResourceAttr, value, allow_fragmented = False, min_bound = None, max_bound = None):
    #     if not allow_fragmented:
    #         return super().get_pth(by, value)
    #     id = self.get_db_id(by, value)
    #     if min_bound is None or max_bound is None:
    #         qry = """
    #         select pth from fragmented_pcds where parent_id = ?;
    #         """
    #         result = database.fetchall(qry, [id])
    #         if result == []:
    #             return super().get_pth(by, value)
    #         return [each[0] for each in result]
    #     else:
    #         qry = """
    #         select pth from fragmented_pcds where not (max_bound_x  < ? or  min_bound_x > ?) and not (max_bound_y  < ? or  min_bound_x > ?);
    #         """
    #         result = database.fetchall(qry, [
    #             max_bound[0], min_bound[0], max_bound[1], min_bound[0]
    #         ])

    
    
   