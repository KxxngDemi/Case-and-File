import tkinter as tk
import os
import subprocess
import sqlite3

from tkinter import messagebox
from typing import List, Optional
from user_info import *


class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.users: List[User] = []
        self.current_user: Optional[User] = None
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        self.master.title("Case and File")
        self.master.geometry("400x300")
        self.grid(sticky="nsew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.pnl_command = tk.Frame(self)
        self.pnl_display = tk.Frame(self)
        
        self.pnl_command.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.pnl_display.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    def create_widgets(self):
        welcome_label = tk.Label(
            self.pnl_command,
            text="Welcome To Case and File",
            font=("Times New Roman", 20, "bold")
        )
        welcome_label.pack(pady=10)

        self.sign_in_btn = tk.Button(
            self.pnl_display,
            text="Sign In",
            command=self.show_sign_in_window,
            width=15
        )
        self.sign_in_btn.pack(pady=5)
    
        self.exit_btn = tk.Button(
            self.pnl_display,
            text="Exit",
            command=self.quit,
            width=15
        )
        self.exit_btn.pack(pady=5)
                
    def show_sign_in_window(self):
        SignInWindow(self)

class SignInWindow(tk.Toplevel):
    def __init__(self, home_page):
        super().__init__(home_page.master)
        self.home_page = home_page
        self.title("Sign In")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Sign In", command=self.attempt_sign_in).pack(pady=10)

    def attempt_sign_in(self):
        name = self.name_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('to_do.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name, password FROM users WHERE name = ? AND password = ?", (name , password))

        user_row = cursor.fetchone()
        
        if user_row:
            name, password = user_row
            user = User(name=name, password=password)
                                
            self.home_page.current_user = user
            messagebox.showinfo("Success", f"Welcome back, {user.name}!")  
            self.destroy()
            todo = subprocess.Popen(
            ['python3', 'to_do_list.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, 
            text=True
        )
            stdout, stderr = todo.communicate()
        else: 
            messagebox.showerror("Error", "Invalid name or password")
                

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(master=root)
    app.mainloop()
