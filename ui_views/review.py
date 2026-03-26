import tkinter as tk
from tkinter import messagebox
from db.queries import insert_review


def leave_review(transaction_id, author_id, target_id, post_id):
    """Allow a user (buyer/seller) to leave a review for the other party."""
    review_window = tk.Toplevel()
    review_window.title("Leave Review")
    review_window.geometry("400x400")

    tk.Label(review_window, text="Leave a Review", font=("Comic Sans MS", 16)).pack(pady=10)
    tk.Label(review_window, text="Satisfaction (1-5):", font=("Comic Sans MS", 14), bg="#ffffff", fg="#333333").pack(pady=5)
    satisfaction_var = tk.DoubleVar(value=3.0)
    tk.Entry(review_window, textvariable=satisfaction_var).pack()

    tk.Label(review_window, text="Review Content:", font=("Comic Sans MS", 14), bg="#ffffff", fg="#333333").pack(pady=5)
    review_content_var = tk.StringVar()
    tk.Entry(review_window, textvariable=review_content_var, width=50).pack()

    def submit_review():
        """Submit a review for the transaction and update the target user's TransactionSatisfaction."""
        # Validate satisfaction score
        if satisfaction_var.get() < 1.0 or satisfaction_var.get() > 5.0:
            messagebox.showerror("Error", "Satisfaction rating must be between 1.0 and 5.0")
            return
        # Validate review content
        if not review_content_var.get().strip():
            messagebox.showerror("Error", "Review content cannot be empty.")
            return
        try:
            insert_review(
                transaction_id, author_id, target_id, post_id,
                satisfaction_var.get(), review_content_var.get()
            )
            messagebox.showinfo("Success", "Review submitted successfully!")
            review_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit review: {e}")

    tk.Button(review_window, text="Submit Review", command=submit_review).pack(pady=20)
