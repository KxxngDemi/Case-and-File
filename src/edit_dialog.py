from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from db_controller import *
from datetime import datetime

class EditDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.controller = DbController("to_do.db")

        self.description_label = QLabel("Description:")
        self.description_line_edit = QLineEdit()
        self.deadline_label = QLabel("Deadline: ")
        self.deadline_calendar_widget = QCalendarWidget()
        self.deadline_calendar_widget.setMinimumDate(datetime.today())
        self.no_deadline_checkbox = QCheckBox("No deadline")

        self.description_deadline_layout = QVBoxLayout()
        self.description_deadline_layout.addWidget(self.description_label)
        self.description_deadline_layout.addWidget(self.description_line_edit)
        self.description_deadline_layout.addWidget(self.deadline_label)
        self.description_deadline_layout.addWidget(self.deadline_calendar_widget)
        self.description_deadline_layout.addWidget(self.no_deadline_checkbox)

        self.save_edit_button = QPushButton("Save")
        self.save_edit_button.setEnabled(False)
        self.cancel_edit_button = QPushButton("Cancel")

        self.edit_button_layout = QHBoxLayout()
        self.edit_button_layout.addWidget(self.save_edit_button)
        self.edit_button_layout.addWidget(self.cancel_edit_button)

        self.description_line_edit.textEdited.connect(self.enable_save_button)
        self.deadline_calendar_widget.clicked.connect(self.enable_save_button)
        self.no_deadline_checkbox.clicked.connect(self.toggle_calendar)
        self.no_deadline_checkbox.clicked.connect(self.enable_save_button)
        self.cancel_edit_button.clicked.connect(self.close)

    def enable_save_button(self):
        self.save_edit_button.setEnabled(True)

    def toggle_calendar(self):
        if self.no_deadline_checkbox.isChecked():
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setEnabled(True)

    def show_confirmation_message(self, message):
        confirmation_dialog = QMessageBox()
        confirmation_dialog.setWindowTitle(" ")
        confirmation_dialog.setInformativeText(message)
        confirmation_dialog.exec_()


class EditTaskDialog(EditDialog):

    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

        self.setWindowTitle("Edit Task")

        self.task_details = self.get_task_details()

        self.description_line_edit.setText(self.task_details[0][1])
        if self.task_details[0][2] is None:
            self.no_deadline_checkbox.setChecked(True)
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setSelectedDate(QDate.fromString(self.task_details[0][2], "yyyy-MM-dd"))

        self.project_assign_label = QLabel("Assign to Project")
        self.project_assign_combobox = QComboBox()
        self.project_assign_combobox.addItem("None")
        project_list = self.get_project_list()
        self.current_index = 0
        for project in project_list:
            self.project_assign_combobox.addItem(project)
            if int(project[0]) == self.task_details[0][5]:
                self.current_index = project_list.index(project) + 1
        self.project_assign_combobox.setCurrentIndex(self.current_index)

        self.project_assign_layout = QVBoxLayout()
        self.project_assign_layout.addWidget(self.project_assign_label)
        self.project_assign_layout.addWidget(self.project_assign_combobox)

        self.edit_task_layout = QVBoxLayout()
        self.edit_task_layout.addLayout(self.description_deadline_layout)
        self.edit_task_layout.addLayout(self.project_assign_layout)
        self.edit_task_layout.addLayout(self.edit_button_layout)

        self.setLayout(self.edit_task_layout)

        self.project_assign_combobox.activated.connect(self.enable_save_button)
        self.save_edit_button.clicked.connect(self.edit_task)

    def get_task_details(self):
        return self.controller.get_single_task(self.task_id)

    def get_project_list(self):
        return [f"{entry[0]}: {entry[1]}" for entry in self.controller.get_all_projects()]

    def edit_task(self):
        description = self.description_line_edit.text() if self.description_line_edit.textEdited else None
        deadline = None if self.no_deadline_checkbox.isChecked() else self.deadline_calendar_widget.selectedDate().toPyDate()
        project_id = None if self.project_assign_combobox.currentText() == "None" else int(self.project_assign_combobox.currentText()[0])

        if description:
            self.controller.edit_task_description(self.task_id, description)
        if deadline:
            self.controller.set_task_deadline(self.task_id, deadline)
        if project_id != self.current_index:
            self.controller.assign_task_to_project(self.task_id, project_id)

        self.show_confirmation_message("Task updated successfully.")
        self.close()


class EditProjectDialog(EditDialog):

    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id

        self.setWindowTitle("Edit Project")

        self.project_details = self.get_project_details()

        self.description_line_edit.setText(self.project_details[0][1])
        if self.project_details[0][2] is None:
            self.no_deadline_checkbox.setChecked(True)
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setSelectedDate(QDate.fromString(self.project_details[0][2], "yyyy-MM-dd"))
        
        self.edit_project_layout = QVBoxLayout()
        self.edit_project_layout.addLayout(self.description_deadline_layout)
        self.edit_project_layout.addLayout(self.edit_button_layout)

        self.setLayout(self.edit_project_layout)

        self.save_edit_button.clicked.connect(self.edit_project)

    def get_project_details(self):
        return self.controller.get_single_project(self.project_id)

    def edit_project(self):
        description = self.description_line_edit.text() if self.description_line_edit.textEdited else None
        deadline = None if self.no_deadline_checkbox.isChecked() else self.deadline_calendar_widget.selectedDate().toPyDate()

        if description:
            self.controller.edit_project_description(self.project_id, description)
        if deadline:
            self.controller.set_project_deadline(self.project_id, deadline)

        self.show_confirmation_message("Project updated successfully.")
        self.close()
