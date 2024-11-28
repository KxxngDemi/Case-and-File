import sqlite3
import os

def create_new_db():
    """Sets up tables for a new database"""
    db_path = 'to_do.db'

    # Check if the file already exists and prompt the user
    
    # Create a new database
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        # Create tasks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INTEGER PRIMARY KEY,
            Description TEXT NOT NULL,
            Deadline DATE,
            Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Completed TIMESTAMP,
            ProjectID INTEGER,
            FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID)
        );
        """)

        # Create projects table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Projects (
            ProjectID INTEGER PRIMARY KEY,
            Description TEXT NOT NULL,
            Deadline DATE,
            Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Completed TIMESTAMP
        );
        """)
        
        # Create user table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """)

        cursor.execute("""
            INSERT INTO users (name, password)
            VALUES ('Kingdom_Chambers', 'password123')
        """)

        connection.commit()
        print("Database and tables created successfully.")

if __name__ == "__main__":
    create_new_db()
