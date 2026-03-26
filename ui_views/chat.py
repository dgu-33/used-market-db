import tkinter as tk
from tkinter import messagebox
from db.queries import get_chat_messages, insert_chat_message


def open_chat_window(post_id, current_user_id, other_user_id):
    """Open a chat window for the given post and participants."""
    try:
        messages = get_chat_messages(post_id, current_user_id, other_user_id)
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to open chat: {e}")
        return

    # Open chat window
    chat_window = tk.Toplevel()
    chat_window.title("Chat")
    chat_window.geometry("600x400")

    # Chat display area
    chat_display = tk.Text(chat_window, state='disabled', wrap='word')
    chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Populate previous messages
    chat_display.config(state='normal')
    for msg in messages:
        chat_display.insert('end', f"{msg['SenderNickname']} ({msg['Timestamp']}): {msg['Message']}\n")
    chat_display.config(state='disabled')

    # Input field and send button
    input_frame = tk.Frame(chat_window)
    input_frame.pack(fill=tk.X, padx=10, pady=10)
    message_var = tk.StringVar()

    def send_message():
        """Handle sending a message."""
        message_text = message_var.get().strip()
        if not message_text:
            messagebox.showerror("Error", "Message cannot be empty.")
            return
        try:
            insert_chat_message(current_user_id, other_user_id, post_id, message_text)
            # Update chat display with new message
            chat_display.config(state='normal')
            chat_display.insert('end', f"You: {message_text}\n")
            chat_display.config(state='disabled')
            message_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    tk.Entry(input_frame, textvariable=message_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    tk.Button(input_frame, text="Send", command=send_message).pack(side=tk.RIGHT)
