import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
from ui_views.chat import open_chat_window
from db.queries import (
    search_posts as db_search_posts,
    get_post_details,
    toggle_like,
    get_buyer_by_nickname,
    update_post as db_update_post,
    insert_transaction_and_update_post,
    delete_post as db_delete_post,
)

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def search_posts(tree, title_var, neighborhood_var, category_var, min_price_var, max_price_var, status_var, likes_var):
    """Read filter variables, execute search, and populate the Treeview."""
    title = title_var.get()
    neighborhood = neighborhood_var.get()
    category = category_var.get()
    min_price = int(min_price_var.get()) if min_price_var.get().isdigit() else 0
    max_price = int(max_price_var.get()) if max_price_var.get().isdigit() else 999999
    status = status_var.get()
    min_likes = int(likes_var.get()) if likes_var.get().isdigit() else 0

    try:
        results = db_search_posts(title, neighborhood, category, min_price, max_price, status, min_likes)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    # Clear existing rows from the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Add results to the Treeview
    for post in results:
        tree.insert("", "end", values=(
            post["PostID"], post["Title"], post["Price"], post["Status"], post["LikesCount"],
            post["Category"], post["Neighborhood"], post["PostDate"]
        ))


def show_post_details(event, current_user_id):
    """Display post details when an item is double-clicked in the Treeview."""
    tree = event.widget
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No post selected.")
        return

    # Retrieve post data from the Treeview
    post = tree.item(selected_item[0], "values")
    try:
        post_id = post[0]  # PostID is the first column
        title = post[1]
        price = post[2]
        status = post[3]
        likes = post[4]
        category = post[5]
        neighborhood = post[6]
    except IndexError:
        messagebox.showerror("Error", "Post data is incomplete.")
        return

    try:
        result = get_post_details(post_id)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load post details: {e}")
        return

    if not result:
        messagebox.showerror("Error", "Post details not found.")
        return

    # Retrieve post information
    description = result.get("Description", "No description available.")
    main_photo = result.get("MainPhoto", None)
    likes_count = result.get("LikesCount", 0)
    post_owner_id = result.get("UserID")

    # Build the image path
    image_folder = os.path.join(_PROJECT_ROOT, "assets", "images")
    image_path = os.path.join(image_folder, main_photo) if main_photo else None

    # Create the detail window
    detail_window = tk.Toplevel(event.widget)
    detail_window.title(f"Details: {title}")
    detail_window.geometry("700x900")
    detail_window.configure(bg="#ffffff")

    # Header
    header_frame = tk.Frame(detail_window, bg="#ff7f0e", height=80)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Post Details", font=("Comic Sans MS", 20, "bold"), bg="#ff7f0e", fg="#ffffff").pack(pady=20)

    if main_photo and image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(detail_window, image=photo).pack(pady=10)
            detail_window.photo = photo
        except Exception:
            tk.Label(detail_window, text="Error loading photo.", font=("Comic Sans MS", 12)).pack(pady=10)
    else:
        tk.Label(detail_window, text="Photo not available.", font=("Comic Sans MS", 12)).pack(pady=10)

    # Detail list
    details = {
        "Title": title,
        "Price": f"${price}",
        "Status": status,
        "Likes": likes_count,
        "Category": category,
        "Neighborhood": neighborhood,
        "Description": description,
    }
    for key, value in details.items():
        tk.Label(detail_window, text=f"{key}: {value}", font=("Comic Sans MS", 12)).pack(anchor="w", padx=20, pady=5)

    # Check ownership and configure buttons
    if post_owner_id == current_user_id:
        # Show "Edit Post" button if the current user owns the post
        tk.Button(
            detail_window, text="Edit Post",
            command=lambda: open_edit_post_window(current_user_id, post_id, title, price, status, description, main_photo, category)
        ).pack(pady=10)
    else:
        # Show "Send Message" and "Like" buttons for other users
        def send_message():
            """Open a chat window with the post owner."""
            if not current_user_id:
                messagebox.showerror("Error", "You must be logged in to send a message.")
                return
            open_chat_window(post_id, current_user_id, post_owner_id)

        def like_product():
            """Toggle the like status on the post."""
            if not current_user_id:
                messagebox.showerror("Error", "You must be logged in to leave a like!")
                return
            try:
                now_liked = toggle_like(current_user_id, post_id)
                if now_liked:
                    messagebox.showinfo("Liked", f"You liked {title}!")
                    like_button.config(text="Unlike")
                else:
                    messagebox.showinfo("Unliked", f"You unliked {title}.")
                    like_button.config(text="Like")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to toggle like status: {e}")

        tk.Button(detail_window, text="Send Message", command=send_message).pack(pady=10)
        like_button = tk.Button(detail_window, text="Like", command=like_product)
        like_button.pack(pady=10)


def open_edit_post_window(current_user_id, post_id, title, price, status, description, main_photo, category):
    """Open a window for editing post details."""
    edit_window = tk.Toplevel()
    edit_window.title("Edit Post")
    edit_window.geometry("500x700")

    tk.Label(edit_window, text="Edit Post", font=("Comic Sans MS", 18, "bold")).pack(pady=10)

    status_choices = ["Available", "Reserved", "Sold"]
    category_choices = ["Appliances", "Electronics", "Toys", "Furniture"]

    fields = {
        "Title": title,
        "Price": price,
        "Description": description,
        "MainPhoto": main_photo,
    }
    entries = {}

    for key, value in fields.items():
        tk.Label(edit_window, text=key, font=("Comic Sans MS", 12)).pack(anchor="w", padx=20, pady=5)
        entry = tk.Entry(edit_window, font=("Comic Sans MS", 12))
        entry.insert(0, value)
        entry.pack(fill=tk.X, padx=20)
        entries[key] = entry

    tk.Label(edit_window, text="Status", font=("Comic Sans MS", 12)).pack(anchor="w", padx=20, pady=5)
    status_var = tk.StringVar(value=status)
    ttk.Combobox(edit_window, textvariable=status_var, values=status_choices, state="readonly").pack(fill=tk.X, padx=20)

    tk.Label(edit_window, text="Category", font=("Comic Sans MS", 12)).pack(anchor="w", padx=20, pady=5)
    category_var = tk.StringVar(value=category)
    ttk.Combobox(edit_window, textvariable=category_var, values=category_choices, state="readonly").pack(fill=tk.X, padx=20)

    def save_changes():
        """Save changes to the database."""
        updated = {key: entry.get().strip() for key, entry in entries.items()}
        updated["Status"] = status_var.get()
        updated["Category"] = category_var.get()

        try:
            if updated["Status"] == "Sold":
                # Prompt the seller to enter the buyer's nickname
                buyer_nickname = simpledialog.askstring("Buyer Nickname", "Enter the Buyer's Nickname:")
                if not buyer_nickname:
                    messagebox.showerror("Error", "Buyer nickname is required to mark this post as sold.")
                    return

                # Look up the buyer by nickname and get their UserID
                buyer_id = get_buyer_by_nickname(buyer_nickname)
                if not buyer_id:
                    messagebox.showerror("Error", f"Buyer with nickname '{buyer_nickname}' does not exist.")
                    return

                # Insert transaction and update post atomically
                insert_transaction_and_update_post(
                    post_id, current_user_id, buyer_id,
                    updated["Title"], updated["Price"], updated["Status"],
                    updated["Description"], updated["MainPhoto"], updated["Category"]
                )
                messagebox.showinfo("Transaction Created", f"Transaction with Buyer '{buyer_nickname}' has been saved.")
            else:
                # Update post details in the Post table
                db_update_post(
                    post_id, updated["Title"], updated["Price"], updated["Status"],
                    updated["Description"], updated["MainPhoto"], updated["Category"]
                )

            messagebox.showinfo("Success", "Post updated successfully!")
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update post: {e}")

    def delete_post():
        """Delete the post from the database."""
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this post?")
        if not confirm:
            return
        try:
            db_delete_post(post_id)
            messagebox.showinfo("Success", "Post deleted successfully!")
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete post: {e}")

    tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=10)
    tk.Button(edit_window, text="Delete Post", command=delete_post).pack(pady=10)
