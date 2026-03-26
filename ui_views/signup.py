import re
import tkinter as tk
from tkinter import messagebox
import bcrypt
from db.queries import insert_user


def validate_inputs(user_data):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, user_data["Email"]):          # Check email format is valid
        messagebox.showerror("Error", "Invalid email format.")
        return False
    if not user_data["Phone Number"].isdigit():             # Check phone number contains only digits
        messagebox.showerror("Error", "Phone Number must contain only digits.")
        return False
    return True


def show_signup_window(app):
    """Display the sign up window."""
    signup_window = tk.Toplevel(app)
    signup_window.title("Sign Up")
    signup_window.geometry("600x800")
    signup_window.configure(bg="#ffffff")

    header_frame = tk.Frame(signup_window, bg="#ff7f0e", height=100)
    header_frame.pack(fill="x")
    tk.Label(
        header_frame, text="Sign Up", font=("Comic Sans MS", 24, "bold"), bg="#ff7f0e", fg="#ffffff"
    ).pack(pady=20)

    form_frame = tk.Frame(signup_window)
    form_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Define input fields
    fields = [
        "UserID",
        "Password",
        "Name",
        "Age",
        "Nickname",
        "Email",
        "Phone Number",
        "Primary Neighborhood"
    ]

    entries = {}
    for field in fields:
        tk.Label(form_frame, text=f"{field}:", font=("Comic Sans MS", 14), bg="#ffffff", fg="#333333").pack(anchor="w", pady=5)
        entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), bg="#f8f8f8", fg="#333333")
        entry.pack(fill="x", pady=5)
        entries[field] = entry

    entries["Password"].config(show="*")

    def submit_signup():
        """Submit the sign up form."""
        user_data = {field: entry.get() for field, entry in entries.items()}
        if not all(user_data.values()):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        try:
            user_data["Age"] = int(user_data["Age"])
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return
        if not validate_inputs(user_data):
            return
        try:
            hashed_pw = bcrypt.hashpw(user_data["Password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            insert_user(
                user_data["UserID"], hashed_pw, user_data["Name"], user_data["Age"],
                user_data["Nickname"], user_data["Email"], user_data["Phone Number"],
                user_data["Primary Neighborhood"]
            )
            messagebox.showinfo("Success", "Sign Up successful!")
            signup_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Sign up failed: {e}")

    tk.Button(
        form_frame,
        text="Submit",
        font=("Comic Sans MS", 14, "bold"),
        bg="#ff7f0e",
        fg="#ffffff",
        command=submit_signup,
    ).pack(pady=20)

    footer_frame = tk.Frame(signup_window, bg="#ff7f0e", height=50)
    footer_frame.pack(fill="x")
    tk.Label(
        footer_frame, text="Welcome to 동국 중고 마켓!", font=("Comic Sans MS", 12), bg="#ff7f0e", fg="#ffffff"
    ).pack(pady=10)
