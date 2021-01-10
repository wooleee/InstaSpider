import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, **kwargs):
        self.db_name = "./database/" + kwargs["db_name"]
        self.table_name = kwargs["table_name"]
        self.recreate = kwargs["recreate"]
        self.start()
        self.create_table()

    def create_table(self):
        r"""
        id INTEGER: id 
        tag TEXT: searched tag
        postlink TEXT: post link 
        post TEXT: post
        imgs TEXT: image links of the post
        othertags TEXT: other tags that linked
        uid INTEGER: hashed userid
        date TEXT: time of the post (%Y-%m-%d)
        likes INTEGER: likes of the post
        """
        sql = f"""CREATE TABLE {self.table_name} (
            id INTEGER PRIMARY KEY, 
            tag TEXT, postlink TEXT, post TEXT, 
            imgs TEXT, othertags TEXT, uid INTEGER, 
            date TEXT, likes INTEGER)"""
        c = self.get_cursor()
        res = c.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE name='{self.table_name}'")
        exist = res.fetchone()[0]
        if (exist == 0) and (not self.recreate):
            c.execute(sql)
            print(f"[INFO] Table: {self.table_name} created.")
        elif (exist == 0) and (self.recreate):
            raise Exception("Table not exists, cannot recreate.")
        elif (exist == 1) and (self.recreate):
            c.execute(f"DROP TABLE {self.table_name}")
            c.execute(sql)
            print(f"[INFO] Table: {self.table_name} recreated.")
        else:  
            # (exist == 1) and (not recreate)
            # means don't need to create table
            print(f"[INFO] Table: {self.table_name} exists.")
            pass
        c.close()
    
    def get_cursor(self):
        c = self.conn.cursor()
        return c

    def insert(self, batch: List[Tuple]):
        """insert into database

        Args:
            batch (List[Tuple]): contains following datas
                idx: int
                tag: str
                postlink: str
                post: str
                imgs: str
                othertags: str
                uid: int
                date: str
                likes: int
        """        
        c = self.get_cursor()
        sql = f"""INSERT INTO {self.table_name} VALUES (?,?,?,?,?,?,?,?,?)"""
        c.executemany(sql, batch)
        c.close()

    def commit(self):
        self.conn.commit()
    
    def close(self):   
        self.conn.close()

    def start(self):
        self.conn = sqlite3.connect(self.db_name)

    def get_last_id(self):
        sql = f"""SELECT id FROM {self.table_name}
            WHERE id = (SELECT MAX(id) FROM {self.table_name})"""
        c = self.get_cursor()
        res = c.execute(sql).fetchall()
        return res 

    def extract_to_folder(self):
        # TODO: extract all datas to a folder
        pass