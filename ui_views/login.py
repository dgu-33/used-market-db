import tkinter as tk
from tkinter import messagebox
import bcrypt
from db.queries import get_user_by_identity


def show_login_window(app):
    # Create login window
    login_window = tk.Toplevel(app)
    login_window.title("Log In")
    login_window.geometry("400x400")
    login_window.configure(bg="#ffffff")

    # ID label and input field
    tk.Label(login_window, text="ID:").pack(pady=5)
    ID_entry = tk.Entry(login_window)
    ID_entry.pack(pady=5)

    # Password label and input field
    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")  # Hide password input
    password_entry.pack(pady=5)

    def login():                   # Function to handle login action
        ID = ID_entry.get()
        password = password_entry.get()

        if not ID or not password:
            messagebox.showerror("Error", "Both ID and Password are required!")
            return

        try:
            user = get_user_by_identity(ID)
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # Check password match
                app.current_user_id = user[0]  # Store logged-in UserID
                messagebox.showinfo("Success", f"Welcome, {user[0]}!")
                login_window.destroy()
                # Update menu state
                app.update_account_menu()
            else:
                messagebox.showerror("Error", "Invalid ID or Password.")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
            print(f"Database error: {e}")

    # Button section
    button_frame = tk.Frame(login_window, bg="#ffffff")
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Log In",
        font=("Comic Sans MS", 14, "bold"),
        bg="#ff7f0e",
        fg="#ffffff",
        width=15,
        command=login
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Cancel",
        font=("Comic Sans MS", 14, "bold"),
        bg="#ffffff",
        fg="#ff7f0e",
        width=15,
        command=login_window.destroy,
    ).pack(pady=10)
