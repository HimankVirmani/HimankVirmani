import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox

# Database setup
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

# User registration
def register_user(username, password):
    conn = create_connection()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        with conn:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        messagebox.showinfo("Success", "User  registered successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose another.")
    finally:
        conn.close()

# User login
def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    
    if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    
    conn.close()

# GUI application
class UserAuthApp:
    def _init_(self, master):
        self.master = master
        master.title("User  Authentication")

        self.label = tk.Label(master, text="Choose an option:")
        self.label.pack()

        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()

    def register(self):
        self.clear_window()
        self.username_label = tk.Label(self.master, text="Enter username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Enter password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show='*')
        self.password_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_registration)
        self.submit_button.pack()

    def submit_registration(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        register_user(username, password)
        self.clear_window()
        self.create_main_buttons()

    def login(self):
        self.clear_window()
        self.username_label = tk.Label(self.master, text="Enter username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Enter password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show='*')
        self.password_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_login)
        self.submit_button.pack()

    def submit_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        login_user(username, password)
        self.clear_window()
        self.create_main_buttons()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_main_buttons(self):
        self.label = tk.Label(self.master, text="Choose an option:")
        self.label.pack()

        self.register_button = tk.Button(self.master, text="Register", command=self.register)
        self.register_button.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack()

if _name_ == "_main_":
    conn = create_connection()
    create_table(conn)
    conn.close()

    root = tk.Tk()
    app = UserAuthApp(root)
    root.mainloop()
