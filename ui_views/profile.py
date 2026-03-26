import tkinter as tk
from tkinter import ttk, messagebox
from ui_views.chat import open_chat_window
from ui_views.review import leave_review
from ui_views.search_view_post import show_post_details
from db.queries import (
    get_user_profile, get_received_reviews, get_user_posts,
    get_user_chats, get_user_transactions
)


def show_profile(app):
    """Display the logged-in user's profile in an orange-and-white modern design."""
    if not app.current_user_id:
        messagebox.showerror("Error", "You must be logged in to view your profile.")
        return

    profile_window = tk.Toplevel(app)
    profile_window.title("Profile")
    profile_window.geometry("800x600")
    profile_window.configure(bg="#ffffff")

    canvas = tk.Canvas(profile_window, bg="#ffffff", highlightthickness=0)
    scrollbar = ttk.Scrollbar(profile_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    try:
        # Fetch user basic info
        user = get_user_profile(app.current_user_id)
        if not user:
            messagebox.showerror("Error", "Failed to retrieve user information.")
            return

        # User info section
        details_frame = tk.Frame(scrollable_frame, bg="#ff7f0e", bd=2, relief="groove")
        details_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            details_frame, text="User Profile", font=("Comic Sans MS", 18, "bold"),
            bg="#ff7f0e", fg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        user_details = [
            f"Nickname: {user['Nickname']}",
            f"Email: {user['Email']}",
            f"Phone Number: {user['PhoneNumber']}",
            f"Transaction Satisfaction: {user['TransactionSatisfaction']}/5",
            f"Primary Neighborhood: {user['PrimaryNeighborhood']}"
        ]
        for detail in user_details:
            tk.Label(
                details_frame, text=detail, font=("Comic Sans MS", 12),
                bg="#ff7f0e", fg="#ffffff"
            ).pack(anchor="w", padx=10, pady=2)

        # Transactions button
        tk.Button(
            details_frame, text="Your Transactions", command=lambda: show_transactions(app),
            font=("Comic Sans MS", 12, "bold"), bg="#ffffff", fg="#ff7f0e", bd=0, padx=10, pady=5
        ).pack(pady=10, padx=10, anchor="w")

        # Reviews section
        tk.Label(
            scrollable_frame, text="Reviews You Received", font=("Comic Sans MS", 16, "bold"),
            bg="#ffffff", fg="#ff7f0e"
        ).pack(anchor="w", padx=20, pady=10)

        received_reviews = get_received_reviews(app.current_user_id)
        if received_reviews:
            for review in received_reviews:
                review_frame = tk.Frame(scrollable_frame, bg="#ffffff", bd=1, relief="solid")
                review_frame.pack(fill="x", padx=20, pady=5)
                tk.Label(
                    review_frame, text=f"From: {review['AuthorNickname']}",
                    font=("Comic Sans MS", 12, "bold"), bg="#ffffff", fg="#ff7f0e"
                ).pack(anchor="w", padx=10, pady=5)
                tk.Label(
                    review_frame, text=f"Satisfaction: {review['TransactionSatisfaction']}/5",
                    font=("Comic Sans MS", 11), bg="#ffffff", fg="#555555"
                ).pack(anchor="w", padx=10, pady=2)
                tk.Label(
                    review_frame, text=f"Review: {review['ReviewContent']}",
                    font=("Comic Sans MS", 11, "italic"), bg="#ffffff", fg="#333333"
                ).pack(anchor="w", padx=10, pady=5)
        else:
            tk.Label(
                scrollable_frame, text="No reviews received.", font=("Comic Sans MS", 11, "italic"),
                bg="#ffffff", fg="#777777"
            ).pack(anchor="w", padx=20, pady=5)

        # User's posts section
        tk.Label(
            scrollable_frame, text="Your Posts", font=("Comic Sans MS", 16, "bold"),
            bg="#ffffff", fg="#ff7f0e"
        ).pack(anchor="w", padx=20, pady=10)

        posts_tree = ttk.Treeview(
            scrollable_frame,
            columns=("PostID", "Title", "Price", "Status", "Likes", "Category", "Neighborhood"),
            show="headings", height=10
        )
        for col in ("PostID", "Title", "Price", "Status", "Likes", "Category", "Neighborhood"):
            posts_tree.heading(col, text=col)

        style = ttk.Style()
        style.configure("Treeview", font=("Comic Sans MS", 11))
        style.configure("Treeview.Heading", font=("Comic Sans MS", 12, "bold"))

        # Fetch user's posts
        posts = get_user_posts(app.current_user_id)
        for post in posts:
            posts_tree.insert("", "end", values=(
                post["PostID"], post["Title"], post["Price"], post["Status"],
                post["Likes"], post["Category"], post["Neighborhood"]
            ))
        posts_tree.pack(fill="x", padx=20, pady=5)
        posts_tree.bind("<Double-1>", lambda event: show_post_details(event, app.current_user_id))

        # Chats section
        tk.Label(
            scrollable_frame, text="Your Chatrooms", font=("Comic Sans MS", 16, "bold"),
            bg="#ffffff", fg="#ff7f0e"
        ).pack(anchor="w", padx=20, pady=10)

        chats = get_user_chats(app.current_user_id)
        unique_post_ids = set()
        if chats:
            for chat in chats:
                post_id = chat['PostID']
                if post_id not in unique_post_ids:
                    unique_post_ids.add(post_id)
                    other_user_id = chat['ReceiverID'] if chat['ReceiverID'] != app.current_user_id else chat['SenderID']
                    tk.Button(
                        scrollable_frame,
                        text=f"Chat on Post {post_id}",
                        command=lambda p=post_id, o=other_user_id: open_chat_window(p, app.current_user_id, o),
                        font=("Comic Sans MS", 11), bg="#ff7f0e", fg="#ffffff", bd=0, padx=10, pady=5
                    ).pack(anchor="w", padx=30, pady=2)
        else:
            tk.Label(
                scrollable_frame, text="No chats found.", font=("Comic Sans MS", 11, "italic"),
                bg="#ffffff", fg="#777777"
            ).pack(anchor="w", padx=30, pady=5)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load profile: {e}")


def show_transactions(app):
    """Display the logged-in user's transactions (both as seller and buyer)."""
    if not app.current_user_id:
        messagebox.showerror("Error", "You must be logged in to view your transactions.")
        return

    transactions_window = tk.Toplevel(app)
    transactions_window.title("Your Transactions")
    transactions_window.geometry("600x400")

    try:
        transactions = get_user_transactions(app.current_user_id)
        tk.Label(transactions_window, text="Your Transactions", font=("Comic Sans MS", 16)).pack(pady=10)

        if transactions:
            for transaction in transactions:
                review_exists = transaction['ReviewExists'] > 0  # Check if review has been submitted
                if review_exists:
                    # Show text if review already submitted
                    tk.Label(
                        transactions_window,
                        text=f"{transaction['Title']} ({transaction['Role']}) - Review Submitted",
                        font=("Comic Sans MS", 10, "italic")
                    ).pack(pady=5)
                else:
                    # Create "Leave Review" button if no review yet
                    tk.Button(
                        transactions_window,
                        text=f"{transaction['Title']} ({transaction['Role']}) - Leave Review",
                        command=lambda t=transaction: leave_review(
                            t["TransactionID"],
                            app.current_user_id,
                            t["BuyerID"] if t["Role"] == 'Seller' else t["SellerID"],  # Review target ID
                            t["PostID"]
                        )
                    ).pack(pady=5)
        else:
            # Show message if no transactions found
            tk.Label(transactions_window, text="No transactions found.", font=("Comic Sans MS", 12, "italic")).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load transactions: {e}")
