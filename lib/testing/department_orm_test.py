import sqlite3
from department import Department
import pytest

DB_NAME = 'coffeeshop.db'


class TestDepartment:
    '''Class Department in department.py'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''Drop tables prior to each test.'''
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS employees")
            cursor.execute("DROP TABLE IF EXISTS departments")
            conn.commit()

    def test_creates_table(self):
        '''Contains method "create_table()" that creates table "departments" if it does not exist.'''
        Department.create_table()
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'")
            result = cursor.fetchone()
        assert result is not None

    def test_drops_table(self):
        '''Contains method "drop_table()" that drops table "departments" if it exists.'''
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

        Department.drop_table()

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='departments'
            """)
            result = cursor.fetchone()
        assert result is None

    def test_saves_department(self):
        '''Contains method "save()" that saves a Department instance to the db and assigns the instance an id.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments")
            row = cursor.fetchone()

        assert row is not None
        assert (row[0], row[1], row[2]) == (department.id, department.name, department.location) == (row[0], "Payroll", "Building A, 5th Floor")

    def test_creates_department(self):
        '''Contains method "create()" that creates a new row in the db using parameter data and returns a Department instance.'''
        Department.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments")
            row = cursor.fetchone()

        assert row is not None
        assert (row[0], row[1], row[2]) == (department.id, department.name, department.location) == (row[0], "Payroll", "Building A, 5th Floor")

    def test_updates_row(self):
        '''Contains method "update()" that updates an instance's corresponding db row to match its new attribute values.'''
        Department.create_table()

        department1 = Department.create("Human Resources", "Building C, East Wing")
        id1 = department1.id
        department2 = Department.create("Marketing", "Building B, 3rd Floor")
        id2 = department2.id

        # Assign new values for name and location
        department2.name = "Sales and Marketing"
        department2.location = "Building B, 4th Floor"

        # Persist the updated values
        department2.update()

        # Assert department1 row was not updated
        department = Department.find_by_id(id1)
        assert (department.id, department.name, department.location) == (id1, "Human Resources", "Building C, East Wing") == (department1.id, department1.name, department1.location)

        # Assert department2 row was updated
        department = Department.find_by_id(id2)
        assert (department.id, department.name, department.location) == (id2, "Sales and Marketing", "Building B, 4th Floor") == (department2.id, department2.name, department2.location)

    def test_deletes_row(self):
        '''Contains method "delete()" that deletes the instance's corresponding db row.'''
        Department.create_table()

        department1 = Department.create("Human Resources", "Building C, East Wing")
        id1 = department1.id
        department2 = Department.create("Sales and Marketing", "Building B, 4th Floor")
        id2 = department2.id

        department2.delete()

        # Assert department1 row was not deleted
        department = Department.find_by_id(id1)
        assert (department.id, department.name, department.location) == (id1, "Human Resources", "Building C, East Wing") == (department1.id, department1.name, department1.location)

        # Assert department2 row is deleted
        assert Department.find_by_id(id2) is None

        # Assert department2 object's id is now None
        assert (department2.id, department2.name, department2.location) == (None, "Sales and Marketing", "Building B, 4th Floor")

    def test_instance_from_db(self):
        '''Contains method "instance_from_db()" that takes a table row and returns a Department instance.'''
        Department.create_table()
        Department.create("Payroll", "Building A, 5th Floor")

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM departments")
            row = cursor.fetchone()

        department = Department.instance_from_db(row)
        assert (row[0], row[1], row[2]) == (department.id, department.name, department.location) == (row[0], "Payroll", "Building A, 5th Floor")

    def test_gets_all(self):
        '''Contains method "get_all()" that returns a list of Department instances for every row in the db.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        departments = Department.get_all()

        assert len(departments) == 2
        assert (departments[0].id, departments[0].name, departments[0].location) == (department1.id, "Human Resources", "Building C, East Wing")
        assert (departments[1].id, departments[1].name, departments[1].location) == (department2.id, "Marketing", "Building B, 3rd Floor")

    def test_finds_by_id(self):
        '''Contains method "find_by_id()" that returns a Department instance corresponding to the db row retrieved by id.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        department = Department.find_by_id(department1.id)
        assert (department.id, department.name, department.location) == (department1.id, "Human Resources", "Building C, East Wing")

        department = Department.find_by_id(department2.id)
        assert (department.id, department.name, department.location) == (department2.id, "Marketing", "Building B, 3rd Floor")

        department = Department.find_by_id(0)
        assert department is None

    def test_finds_by_name(self):
        '''Contains method "find_by_name()" that returns a Department instance corresponding to the db row retrieved by name.'''
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        department = Department.find_by_name("Human Resources")
        assert (department.id, department.name, department.location) == (department1.id, "Human Resources", "Building C, East Wing")

        department = Department.find_by_name("Marketing")
        assert (department.id, department.name, department.location) == (department2.id, "Marketing", "Building B, 3rd Floor")

        department = Department.find_by_name("Unknown")
        assert department is None
