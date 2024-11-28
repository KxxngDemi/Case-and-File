from PyQt5.QtWidgets import *
from db_controller import *

class DeleteTaskDialog(QDialog):

    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id
        self.controller = DbController("to_do.db")

        self.setWindowTitle("Delete Task")

        self.delete_task_message_label = QLabel("Are you sure you want to delete the selected task?")

        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        self.delete_task_button_layout = QHBoxLayout()
        self.delete_task_button_layout.addWidget(self.yes_button)
        self.delete_task_button_layout.addWidget(self.no_button)

        self.delete_task_layout = QVBoxLayout()
        self.delete_task_layout.addWidget(self.delete_task_message_label)
        self.delete_task_layout.addLayout(self.delete_task_button_layout)

        self.setLayout(self.delete_task_layout)

        self.yes_button.clicked.connect(self.delete_task)
        self.no_button.clicked.connect(self.close)

    def delete_task(self):
        self.controller.delete_task(self.task_id)
        self.show_confirmation_message("Task deleted")
        self.close()

    def show_confirmation_message(self, message):
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle(" ")
        confirmation_dialog.setInformativeText(message)
        confirmation_dialog.exec_()


class DeleteProjectDialog(QDialog):

    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id
        self.controller = DbController("to_do.db")

        self.setWindowTitle("Delete Project")

        self.delete_project_message_label = QLabel("Delete this project and all associated tasks?")

        self.delete_project_tasks_button = QPushButton("Delete project and tasks")
        self.delete_project_only_button = QPushButton("Delete project only")
        self.delete_project_cancel_button = QPushButton("Cancel")

        self.delete_project_button_layout = QHBoxLayout()
        self.delete_project_button_layout.addWidget(self.delete_project_tasks_button)
        self.delete_project_button_layout.addWidget(self.delete_project_only_button)
        self.delete_project_button_layout.addWidget(self.delete_project_cancel_button)

        self.delete_project_layout = QVBoxLayout()
        self.delete_project_layout.addWidget(self.delete_project_message_label)
        self.delete_project_layout.addLayout(self.delete_project_button_layout)

        self.setLayout(self.delete_project_layout)

        self.delete_project_tasks_button.clicked.connect(self.delete_project_and_tasks)
        self.delete_project_only_button.clicked.connect(self.delete_project_only)
        self.delete_project_cancel_button.clicked.connect(self.close)

    def delete_project_and_tasks(self):
        self.controller.delete_project_and_tasks(self.project_id)
        self.show_confirmation_message("Project and associated tasks deleted")
        self.close()

    def delete_project_only(self):
        self.controller.delete_project_only(self.project_id)
        self.show_confirmation_message("Associated tasks are no longer assigned to any project")
        self.close()

    def show_confirmation_message(self, message):
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle(" ")
        confirmation_dialog.setInformativeText(message)
        confirmation_dialog.exec_()
