import unittest
import sqlite3
import os

from create_new_db import create_new_db  

class TestCreateNewDB(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.db_path = 'to_do.db'
        
        
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        """Clean up after each test."""
        
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_database(self):
        """Test if the database file is created."""
        create_new_db()  
        self.assertTrue(os.path.exists(self.db_path), "Database file should exist after creation.")
        
    def test_create_tables(self):
        """Test if the necessary tables (Tasks, Projects, users) are created."""
        create_new_db()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
       
        
        table_names = [table[0] for table in tables]
        self.assertIn('Tasks', table_names, "Tasks table should be created.")
        self.assertIn('Projects', table_names, "Projects table should be created.")
        self.assertIn('users', table_names, "users table should be created.")

    def test_insert_user(self):
        """Test if the user 'Kingdom_Chambers' is inserted into the users table."""
        create_new_db()

        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM users WHERE name='Kingdom_Chambers';")
            user = cursor.fetchone()
        
        self.assertIsNotNone(user, "User 'Kingdom_Chambers' should be inserted into the users table.")
        self.assertEqual(user[0], 'Kingdom_Chambers', "The inserted user's name should be 'Kingdom_Chambers'.")

     
if __name__ == "__main__":
    unittest.main()
