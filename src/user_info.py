from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from db_controller import *
from radio_button_widget import *
from table_widget import *
from add_new_dialog import *
from mark_complete_dialog import *
from edit_dialog import *
from delete_dialog import *
from project_tasks_dialog import *

class User:
    # Class variable for ID
    id = 0  # Static variable equivalent
    
    def __init__(self, password, f_name, l_name, next_id):
        """Initialize a new User instance."""
        User.id = next_id  # Using class variable
        self.f_name = f_name
        self.l_name = l_name
        self.password = password
        User.id += 1  # Increment the ID

    # Property decorators for getters and setters
    @property
    def id(self):
        """Get the user's ID."""
        return User.id

    @property
    def name(self):
        """Get the user's full name."""
        return f"{self.f_name} {self.l_name}"
    
    @name.setter
    def name(self, names):
        """Set the user's first and last name."""
        self.f_name, self.l_name = names  # Expecting a tuple of (first_name, last_name)

    @property
    def password(self):
        """Get the user's password."""
        return self._password
    
    @password.setter
    def password(self, value):
        """Set the user's password."""
        self._password = value

    def sign_in(self, entered_name, entered_password):
        """
        Verify user credentials.
        
        Args:
            entered_name (str): The TRN number entered by the user
            entered_password (str): The password entered by the user
            
        Returns:
            bool: True if credentials match, False otherwise
        """
        if entered_name == self.name and entered_password == self._password:
            print("Sign-in successful")
            return True
        else:
            print("Invalid name or password")
            return False
