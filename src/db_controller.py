import sqlite3
from datetime import datetime

class DbController:
    def __init__(self, db_name):
        self.db_name = db_name

    def query(self, sql, data):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA Foreign_Keys = ON")
            cursor.execute(sql, data)
            db.commit()

    def select_query(self, sql, data=None):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(sql, data) if data else cursor.execute(sql)
            return cursor.fetchall()

    def add_task(self, description, deadline, project_id):
        created = datetime.now()
        sql = "INSERT INTO Tasks (Description, Deadline, Created, ProjectID) VALUES (?,?,?,?)"
        self.query(sql, (description, deadline, created, project_id))

    def add_project(self, description, deadline):
        created = datetime.now()
        sql = "INSERT INTO Projects (Description, Deadline, Created) VALUES (?,?,?)"
        self.query(sql, (description, deadline, created))

    def delete_task(self, task_id):
        sql = "DELETE FROM Tasks WHERE TaskID = ?"
        self.query(sql, (task_id,))

    def delete_project_only(self, project_id):
        self.query("UPDATE Tasks SET ProjectID = NULL WHERE ProjectID = ?", (project_id,))
        self.query("DELETE FROM Projects WHERE ProjectID = ?", (project_id,))

    def delete_project_and_tasks(self, project_id):
        self.query("DELETE FROM Tasks WHERE ProjectID = ?", (project_id,))
        self.query("DELETE FROM Projects WHERE ProjectID = ?", (project_id,))

    def mark_task_completed(self, task_id):
        completed = datetime.now()
        sql = "UPDATE Tasks SET Completed = ? WHERE TaskID = ?"
        self.query(sql, (completed, task_id))

    def mark_project_completed(self, project_id):
        completed = datetime.now()
        sql = "UPDATE Projects SET Completed = ? WHERE ProjectID = ?"
        self.query(sql, (completed, project_id))

    def mark_project_tasks_completed(self, project_id):
        completed = datetime.now()
        sql = "UPDATE Tasks SET Completed = ? WHERE ProjectID = ?"
        self.query(sql, (completed, project_id))

    def get_task_project_id(self, task_id):
        sql = "SELECT ProjectID FROM Tasks WHERE TaskID = ?"
        return self.select_query(sql, (task_id,))[0][0]

    def check_project_tasks_completed(self, project_id):
        sql = "SELECT TaskID FROM Tasks WHERE ProjectID = ? AND Completed IS NULL"
        return not self.select_query(sql, (project_id,))

    def edit_task_description(self, task_id, description):
        sql = "UPDATE Tasks SET Description = ? WHERE TaskID = ?"
        self.query(sql, (description, task_id))

    def set_task_deadline(self, task_id, deadline):
        sql = "UPDATE Tasks SET Deadline = ? WHERE TaskID = ?"
        self.query(sql, (deadline, task_id))

    def assign_task_to_project(self, task_id, project_id):
        sql = "UPDATE Tasks SET ProjectID = ? WHERE TaskID = ?"
        self.query(sql, (project_id, task_id))

    def set_project_deadline(self, project_id, deadline):
        sql = "UPDATE Projects SET Deadline = ? WHERE ProjectID = ?"
        self.query(sql, (deadline, project_id))

    def edit_project_description(self, project_id, description):
        sql = "UPDATE Projects SET Description = ? WHERE ProjectID = ?"
        self.query(sql, (description, project_id))

    def get_all_tasks(self):
        return self.select_query("SELECT * FROM Tasks")

    def get_active_tasks(self):
        return self.select_query("SELECT * FROM Tasks WHERE Completed IS NULL")

    def get_completed_tasks(self):
        return self.select_query("SELECT * FROM Tasks WHERE Completed IS NOT NULL")

    def get_single_task(self, task_id):
        return self.select_query("SELECT * FROM Tasks WHERE TaskID = ?", (task_id,))

    def get_all_projects(self):
        return self.select_query("SELECT * FROM Projects")

    def get_active_projects(self):
        return self.select_query("SELECT * FROM Projects WHERE Completed IS NULL")

    def get_completed_projects(self):
        return self.select_query("SELECT * FROM Projects WHERE Completed IS NOT NULL")

    def get_single_project(self, project_id):
        return self.select_query("SELECT * FROM Projects WHERE ProjectID = ?", (project_id,))

    def get_project_tasks(self, project_id):
        return self.select_query("SELECT * FROM Tasks WHERE ProjectID = ?", (project_id,))







