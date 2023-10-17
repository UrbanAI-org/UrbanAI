import sqlite3
import queue

from database.singletonMeta import SingletonMeta
from threading import Thread
import os
# global database 
# database = None
class FileChecker:
    def __init__(self) -> None:
        pass

    def run(self):
        self.check_tifs()
        self.check_chunks()
        pass

    def check_tifs(self):
        qry = """
        select * from tifs;"""
        
        pass

    def check_chunks(self):
        pass 

    def check_chunk_pcd(self):
        pass 

    def check_chunk_mesh(self):
        pass

class Database(metaclass=SingletonMeta):

    def __init__(self, db, tables, debug = False) -> None:
        self.work_queue = queue.Queue()
        self.db = db
        self.tables = tables
        self.dbloop = True
        self.debug = debug
        self.cache = {}
        self.hasStart = True
        self.opened = False

    def start(self):
        def run():
            con = sqlite3.connect(self.db, check_same_thread=False)
            cur = con.cursor()
            cur.executescript(self.tables)
            con.commit()
            print("db connected")
            while True and self.dbloop:
                try:
                    (sql, params), result_queue = self.work_queue.get()
                    if sql == "__STOP__":
                        break
                    cur.execute(sql, params)
                    res = cur.fetchall()
                    if self.debug:
                        print("------ SQL WORKER ------")
                        print(sql, params, res, sep="\n")
                        print("-----------------------")
                    con.commit()
                    result_queue.put(res)
                except Exception as e:
                    print(e)
            con.close()
        thread = Thread(target=run)
        thread.start()
        self.opened = True
        
    
    def execute_in_worker(self, sql, params = []):
        if not self.opened:
            raise DatabaseOpened("Database is not opend")
        if self.hasStart:

            # you might not really need the results if you only use this
            # for writing unless you use something like https://www.sqlite.org/lang_returning.html
            try:

                result_queue = queue.Queue()
                self.work_queue.put(((sql, params), result_queue))
                return result_queue.get(timeout=5)
            except queue.Empty:
                raise DatabaseError("Please check your input. If it is current, please concat us.")
        return None

    def fetchall(self, sql, params = []):
        return self.execute_in_worker(sql, params)

    def fetchone(self, sql, params = []):
        res = self.execute_in_worker(sql, params)
        if len(res) == 0:
            return None
        return res[0]
    
    def close(self):
        self.work_queue.put((("__STOP__", []), queue.Queue()))

    def report(self):
        qry = """
        select count(*) from tifs;"""
        result = self.fetchone(qry)
        count_tifs = result[0]
        qry = """
        select count(*) from meshes;"""
        result = self.fetchone(qry)
        count_meshes = result[0]
        qry = """
        select count(*) from chunks;"""
        result = self.fetchone(qry)
        count_regions = result[0]
        print(f"""Database Report:\nThere is {count_tifs} tifs, {count_meshes} Meshes, {count_regions} User Defined Regions""")
        qry = """
        select lat_begin, lat_end, lon_begin, lon_end, filename, origin_lat, origin_lon from tifs order by lat_begin, lon_begin;"""
        result = self.fetchall(qry)
        for each in result:
            print(f"- {each[4]}[{each[5]},{each[6]}]: latitude from {int(each[0])} to {int(each[1])}, longitude from {int(each[2])} to {int(each[3])}.")
        print("")

    def put_cache(self, cache_key, cache_value):
        if len(self.cache.keys()) > 80:
            self.clear_cache()
        self.cache.update({cache_key: cache_value})

    def get_cache(self, cache_key, cache_value = None):
        value = self.cache.get(cache_key)
        if value is None:
            return cache_value
        return value
    
    def remove_cache(self, cache_key):
        if cache_key is not None:
            value = self.cache.get(cache_key)
            if value is not None:
                qry = """
                delete from chunks where id = ?;
                """
                self.execute_in_worker(qry, [value['id']])
                mesh_id = value['mesh_id']
                if mesh_id is not None:
                    pth = self.fetchone("select pth from meshes where id = ?;", [mesh_id])[0]
                    self.execute_in_worker("delete from meshes where id = ?;", [mesh_id])
                    if os.path.exists(pth):
                        os.remove(pth)

    def delete_resource(self, id):
        qry = """
        select id, mesh from chunks where id = ?;
        """
        result = self.fetchone(qry, [id])
        if result is None:
            return
        qry = """
        delete from chunks where id = ?;
        """
        self.execute_in_worker(qry, [result[0]])
        mesh_id = result[1]
        if mesh_id is not None:
            pth = self.fetchone("select pth from meshes where id = ?;", [mesh_id])[0]
            self.execute_in_worker("delete from meshes where id = ?;", [mesh_id])
            if os.path.exists(pth):
                os.remove(pth)

        pass     
    
    def in_cache(self, cache_key):
        return cache_key in self.cache.keys()
    
    def clear_cache(self):
        self.cache = {}
        temp = self.cache
        for key in temp.keys():
            self.remove_cache(key)

    def clear_regions(self):

        # for value in temp.values():
        #     chunk_id = value['id']
        qry = """
        select id from chunks;
        """
        result = self.fetchall(qry)
        self.cache = {}
        for each in result:
            self.delete_resource(each[0])

        #     self.execute_in_worker(qry, [chunk_id])
        #     mesh_id = value['mesh_id']
        #     pth = self.fetchone("select pth from meshes where id = ?;", [mesh_id])[0]
        #     self.execute_in_worker("delete from meshes where id = ?;", [mesh_id])
        #     if os.path.exists(pth):
        #         os.remove(pth)
                
        pass

    # def 

class DatabaseOpened(Exception):
    pass

tables = """
create table if not exists meshes (
    id integer primary key AUTOINCREMENT,
    uid text not null,
    expired integer not null,
    last_update real not null,
    pth text not null
);

create table if not exists pcds (
    id integer primary key AUTOINCREMENT,
    uid text not null,
    expired integer not null,
    last_update real not null,
    pth text not null
);

create table if not exists tifs (
    id integer primary key AUTOINCREMENT,
    uid text not null,
    filename text not null,
    pth text not null,
    origin_lat real not null,
    origin_lon real not null,
    lat_begin integer,
    lat_end integer,
    lon_begin integer,
    lon_end integer,
    pcd integer references pcds(id),
    mesh integer references meshs(id)

);

create table if not exists chunks (
    id text primary key,
    center_x real not null,
    center_y real not null,
    min_bound_x real not null,
    min_bound_y real not null,
    max_bound_x real not null,
    max_bound_y real not null,
    origin_lat real not null,
    origin_lon real not null,
    parent text not null,
    pcd integer references pcds(id),
    mesh integer references meshs(id),
    max_altitude real not null,
    min_altitude real not null

);
"""
# create table if not exists fragmented_pcds (
#     id integer primary key AUTOINCREMENT,
#     min_bound_x real not null,
#     min_bound_y real not null,
#     max_bound_x real not null,
#     max_bound_y real not null,  
#     parent text not null,
#     pth text not null,
#     parent_id integer references pcds(id)


# );
# """

# def start():
global database 
database = Database("urbanAI.db", tables)

class DatabaseError(Exception):
    pass