from lib import CONN, CURSOR

class Department:
    # ... your methods

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """)
        CONN.commit()

    
