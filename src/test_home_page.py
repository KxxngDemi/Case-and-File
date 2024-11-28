import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
import sqlite3
import subprocess
from home_page import HomePage, SignInWindow  

class TestHomePage(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = HomePage(master=self.root)

    def tearDown(self):
        self.root.destroy()

    def test_home_page_initialization(self):
        self.assertEqual(self.app.master.title(), "Case and File")
        self.assertEqual(self.app.pnl_command.winfo_children()[0]['text'], "Welcome To Case and File")
        self.assertTrue(self.app.sign_in_btn.winfo_exists())
        self.assertTrue(self.app.exit_btn.winfo_exists())

    @patch("home_page.SignInWindow")
    def test_sign_in_button_triggers_sign_in_window(self, mock_sign_in_window):
        self.app.sign_in_btn.invoke()
        mock_sign_in_window.assert_called_once_with(self.app)

class TestSignInWindow(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.home_page = HomePage(master=self.root)
        self.sign_in_window = SignInWindow(self.home_page)

    def tearDown(self):
        self.sign_in_window.destroy()
        self.root.destroy()

    @patch("sqlite3.connect")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    def test_attempt_sign_in_success(self, mock_error, mock_info, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("test_user", "test_pass")

        self.sign_in_window.name_entry.insert(0, "test_user")
        self.sign_in_window.password_entry.insert(0, "test_pass")
        self.sign_in_window.attempt_sign_in()

        mock_info.assert_called_once_with("Success", "Welcome back, test_user!")
        mock_error.assert_not_called()

    @patch("sqlite3.connect")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    def test_attempt_sign_in_failure(self, mock_error, mock_info, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        self.sign_in_window.name_entry.insert(0, "wrong_user")
        self.sign_in_window.password_entry.insert(0, "wrong_pass")
        self.sign_in_window.attempt_sign_in()

        mock_error.assert_called_once_with("Error", "Invalid name or password")
        mock_info.assert_not_called()

    @patch("subprocess.Popen")
    def test_subprocess_called_on_sign_in(self, mock_popen):
        with patch("sqlite3.connect") as mock_connect:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = ("test_user", "test_pass")

            mock_process = MagicMock()
            mock_process.communicate.return_value = ("output", "error")  
            mock_popen.return_value = mock_process

            self.sign_in_window.name_entry.insert(0, "test_user")
            self.sign_in_window.password_entry.insert(0, "test_pass")
            self.sign_in_window.attempt_sign_in()

            mock_popen.assert_called_once_with(
                ['python3', 'to_do_list.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            mock_process.communicate.assert_called_once()

if __name__ == "__main__":
    unittest.main()

