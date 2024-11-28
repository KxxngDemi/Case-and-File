from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import json
import os

from db_controller import *
from radio_button_widget import *
from table_widget import *
from add_new_dialog import *
from mark_complete_dialog import *
from edit_dialog import *
from delete_dialog import *
from project_tasks_dialog import *

class User:
         
    def __init__(self, password, name):
        """Initialize a new User instance."""
        self.name = name
        self.password = password
        
    @property
    def name(self):
        """Get the user's full name."""
        return self._name 
    
    @name.setter
    def name(self, full_name):
        """Set the user's first and last name."""
        self._name = full_name  

    @property
    def password(self):
        """Get the user's password."""
        return self._password
    
    @password.setter
    def password(self, value):
        """Set the user's password."""
        self._password = value

    
