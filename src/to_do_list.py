import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from tab_widget import *

class ToDoWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("To Do List")
        self.setMinimumHeight(300)

        self.central_widget = TaskProjectTabs()
        self.setCentralWidget(self.central_widget)

        self.central_widget.task_exit_button.clicked.connect(self.close)
        self.central_widget.project_exit_button.clicked.connect(self.close)

if __name__ == "__main__":
    to_do = QApplication(sys.argv)
    main_window = ToDoWindow()
    main_window.show()
    main_window.raise_()
    to_do.exec_()
