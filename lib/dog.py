import sqlite3

from __init__ import CURSOR, CONN

class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id:
            sql = """
                UPDATE dogs SET name = ?, breed = ? WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
        else:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = Dog(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        results = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in results]
    
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        result = CURSOR.execute(sql, (name,)).fetchone()
        if result:
            return cls.new_from_db(result)
        return None
    
    @classmethod
    def find_by_id(cls, dog_id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        result = CURSOR.execute(sql, (dog_id,)).fetchone()
        if result:
            return cls.new_from_db(result)
        return None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog and dog.breed == breed:
            return dog
        else:
            return cls.create(name, breed)
        
    def update(self):
        if self.id:
            self.save()