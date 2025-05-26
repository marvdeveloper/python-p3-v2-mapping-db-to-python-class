import sqlite3

DB_NAME = 'coffeeshop.db'

class Department:
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    @classmethod
    def create_table(cls):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    location TEXT
                )
            """)
            conn.commit()

    @classmethod
    def drop_table(cls):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS departments")
            conn.commit()

    def save(self):
        if self.id is None:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO departments (name, location) VALUES (?, ?)",
                    (self.name, self.location)
                )
                self.id = cursor.lastrowid
                conn.commit()
        else:
            self.update()

    @classmethod
    def create(cls, name, location):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO departments (name, location) VALUES (?, ?)",
                (name, location)
            )
            conn.commit()
            id = cursor.lastrowid
            return cls(name, location, id=id)

    def update(self):
        if self.id is not None:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE departments SET name = ?, location = ? WHERE id = ?",
                    (self.name, self.location, self.id)
                )
                conn.commit()

    def delete(self):
        if self.id is not None:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM departments WHERE id = ?", (self.id,))
                conn.commit()
            self.id = None

    @classmethod
    def instance_from_db(cls, row):
        # row = (id, name, location)
        return cls(row[1], row[2], id=row[0])

    @classmethod
    def get_all(cls):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments")
            rows = cursor.fetchall()
            return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments WHERE id = ?", (id,))
            row = cursor.fetchone()
            return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments WHERE name = ?", (name,))
            row = cursor.fetchone()
            return cls.instance_from_db(row) if row else None
