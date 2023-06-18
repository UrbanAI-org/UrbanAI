import sqlite3
import queue
from src.database.singletonMeta import SingletonMeta
from threading import Thread

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
        
    
    def execute_in_worker(self, sql, params = []):
        # you might not really need the results if you only use this
        # for writing unless you use something like https://www.sqlite.org/lang_returning.html
        result_queue = queue.Queue()
        self.work_queue.put(((sql, params), result_queue))
        return result_queue.get(timeout=5)

    def fetchall(self, sql, params = []):
        return self.execute_in_worker(sql, params)

    def fetchone(self, sql, params = []):
        res = self.execute_in_worker(sql, params)
        if len(res) == 0:
            return None
        return res[0]
    
    def close(self):
        self.work_queue.put((("__STOP__", []), queue.Queue()))


    def env_check(self, envChecker):
        pass

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
        print(f"""Database Report:\nThere is {count_tifs} tifs, {count_meshes} Meshes, {count_regions} User Defined Regions\n""")
    
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
    lat_begin real,
    lat_end real,
    lon_begin real,
    lon_end real,
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
# def start():
global database 
database = Database("urbanAI.db", tables)

