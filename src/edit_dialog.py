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
        confirmation_dialog.setW
