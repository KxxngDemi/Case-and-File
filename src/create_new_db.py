import sqlite3
import os

def create_new_db():
    """Sets up tables for a new database"""
    db_path = 'to_do.db'

    # Check if the file already exists and prompt the user
    if os.path.exists(db_path):
        print("Database file already exists. Recreating it...")
        os.remove(db_path)

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

        connection.commit()
        print("Database and tables created successfully.")

if __name__ == "__main__":
    create_new_db()
