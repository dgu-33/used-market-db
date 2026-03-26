import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from db.queries import get_user_neighborhood, insert_post


def show_add_product_window(app):
    # Check if user is logged in
    if not hasattr(app, 'current_user_id') or not app.current_user_id:
        messagebox.showerror("Error", "Please log in to add a product.")
        return

    user_id = app.current_user_id  # Get logged-in UserID

    # Create "Add Post" window
    add_post_window = tk.Toplevel(app)
    add_post_window.title("Add Post")
    add_post_window.geometry("600x800")
    add_post_window.configure(bg="#ffffff")

    tk.Label(add_post_window, text="Add Post", font=("Comic Sans MS", 24, "bold"), bg="#ff7f0e", fg="#ffffff").pack(
        pady=20, fill="x"
    )

    form_frame = tk.Frame(add_post_window, bg="#ffffff")
    form_frame.pack(pady=10, padx=20, fill="both", expand=True)

    fields = ["Title", "Category", "Price", "Description", "Main Photo"]
    entries = {}

    for field in fields:
        tk.Label(form_frame, text=f"{field}:", font=("Comic Sans MS", 14)).pack(anchor="w", pady=5)
        if field == "Category":
            category_var = tk.StringVar(value="Select Category")
            category_dropdown = ttk.Combobox(
                form_frame,
                textvariable=category_var,
                values=["Electronics", "Furniture", "Appliances", "Toys", "Others"],
                state="readonly"
            )
            category_dropdown.pack(fill="x", pady=5)
            entries[field] = category_var
        elif field == "Main Photo":
            photo_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12))
            photo_entry.pack(fill="x", pady=5)

            def browse_photo():
                file_path = filedialog.askopenfilename(
                    title="Select Main Photo",
                    filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("All Files", "*.*")]
                )
                photo_entry.delete(0, tk.END)
                photo_entry.insert(0, file_path)

            tk.Button(form_frame, text="Browse", command=browse_photo).pack(pady=5)
            entries[field] = photo_entry
        elif field == "Description":
            description_entry = tk.Text(form_frame, font=("Comic Sans MS", 12), height=5)
            description_entry.pack(fill="x", pady=5)
            entries[field] = description_entry
        else:
            entry = tk.Entry(form_frame, font=("Comic Sans MS", 12))
            entry.pack(fill="x", pady=5)
            entries[field] = entry

    def submit_post():
        # Get logged-in user
        user_id = app.current_user_id
        if not user_id:
            messagebox.showerror("Error", "Please log in to add a post.")
            return

        # Collect post details
        title = entries["Title"].get()
        category = entries["Category"].get()
        price_str = entries["Price"].get()
        price = int(price_str) if price_str.isdigit() else None
        description = entries["Description"].get("1.0", tk.END).strip()
        main_photo = entries["Main Photo"].get()

        if not all([title, category, price, description, main_photo]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Fetch user's PrimaryNeighborhood
            neighborhood = get_user_neighborhood(user_id)
            if not neighborhood:
                messagebox.showerror("Error", "User's neighborhood could not be found.")
                return

            # Insert post into database
            insert_post(user_id, title, category, price, description, main_photo, neighborhood)
            messagebox.showinfo("Success", "Post added successfully!")
            add_post_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(add_post_window, text="Submit", font=("Segoe UI", 14), command=submit_post).pack(pady=20)
