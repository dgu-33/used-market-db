"""
All database query functions.
Each function opens its own connection, executes the query, and closes it.
Raises exceptions on failure — callers are responsible for messagebox display.
"""
from database import get_connection


# ---------------------------------------------------------------------------
# User queries
# ---------------------------------------------------------------------------

def get_user_by_identity(identity):
    """Return (UserID, Password) matching UserID, Email, or PhoneNumber."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT UserID, Password FROM users
            WHERE UserID = %s OR Email = %s OR PhoneNumber = %s
        """, (identity, identity, identity))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_user(user_id, hashed_pw, name, age, nickname, email, phone, neighborhood):
    """Insert a new user row."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (UserID, Password, Name, Age, Nickname, Email, PhoneNumber, PrimaryNeighborhood)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, hashed_pw, name, age, nickname, email, phone, neighborhood))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_user_profile(user_id):
    """Return profile info dict for the given user."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT Nickname, Email, PhoneNumber, TransactionSatisfaction, PrimaryNeighborhood
            FROM users WHERE UserID = %s
        """, (user_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_user_neighborhood(user_id):
    """Return PrimaryNeighborhood for the given user, or None."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT PrimaryNeighborhood FROM users WHERE UserID = %s", (user_id,))
        row = cursor.fetchone()
        return row["PrimaryNeighborhood"] if row else None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_buyer_by_nickname(nickname):
    """Return the UserID of the user with the given nickname, or None."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT UserID FROM users WHERE Nickname = %s", (nickname,))
        row = cursor.fetchone()
        return row["UserID"] if row else None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Post queries
# ---------------------------------------------------------------------------

def search_posts(title, neighborhood, category, min_price, max_price, status, min_likes):
    """Return a list of post dicts matching the given filters."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT PostID, Title, Price, Status, LikesCount, Category, Neighborhood, PostDate
        FROM Post
        WHERE 1=1
          AND (Title LIKE %s OR %s = '')
          AND (%s = 'All' OR Category = %s)
          AND (Neighborhood = %s OR %s = '')
          AND (Price BETWEEN %s AND %s)
          AND (%s = 'All' OR Status = %s)
          AND (LikesCount >= %s)
        """
        params = (
            f"%{title}%", title,
            category, category,
            neighborhood, neighborhood,
            min_price, max_price,
            status, status,
            min_likes,
        )
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_post_details(post_id):
    """Return a dict with Description, MainPhoto, LikesCount, UserID for the post."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT Description, MainPhoto, LikesCount, UserID FROM Post WHERE PostID = %s",
            (post_id,)
        )
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_post(user_id, title, category, price, description, main_photo, neighborhood):
    """Insert a new Post row."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Post (UserID, Title, Category, Price, Description, MainPhoto, Status, LikesCount, Neighborhood)
            VALUES (%s, %s, %s, %s, %s, %s, 'Available', 0, %s)
        """, (user_id, title, category, price, description, main_photo, neighborhood))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_post(post_id, title, price, status, description, main_photo, category):
    """Update an existing Post row."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Post
            SET Title = %s, Price = %s, Status = %s, Description = %s, MainPhoto = %s, Category = %s
            WHERE PostID = %s
        """, (title, price, status, description, main_photo, category, post_id))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_transaction_and_update_post(post_id, seller_id, buyer_id,
                                       title, price, status, description, main_photo, category):
    """Insert a transaction record and update the post atomically."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Transactions (PostID, SellerID, BuyerID)
            VALUES (%s, %s, %s)
        """, (post_id, seller_id, buyer_id))
        cursor.execute("""
            UPDATE Post
            SET Title = %s, Price = %s, Status = %s, Description = %s, MainPhoto = %s, Category = %s
            WHERE PostID = %s
        """, (title, price, status, description, main_photo, category, post_id))
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def delete_post(post_id):
    """Delete a Post row."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Post WHERE PostID = %s", (post_id,))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def toggle_like(user_id, post_id):
    """Toggle the like status for a user on a post.
    Returns True if the post is now liked, False if unliked.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM UserLikes WHERE UserID = %s AND PostID = %s",
            (user_id, post_id)
        )
        liked = cursor.fetchone()
        if liked:
            cursor.execute(
                "DELETE FROM UserLikes WHERE UserID = %s AND PostID = %s",
                (user_id, post_id)
            )
            cursor.execute(
                "UPDATE Post SET LikesCount = LikesCount - 1 WHERE PostID = %s",
                (post_id,)
            )
            conn.commit()
            return False  # now unliked
        else:
            cursor.execute(
                "INSERT INTO UserLikes (UserID, PostID) VALUES (%s, %s)",
                (user_id, post_id)
            )
            cursor.execute(
                "UPDATE Post SET LikesCount = LikesCount + 1 WHERE PostID = %s",
                (post_id,)
            )
            conn.commit()
            return True  # now liked
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Profile queries
# ---------------------------------------------------------------------------

def get_user_posts(user_id):
    """Return all posts by the given user."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT PostID, Title, Price, Status, LikesCount AS Likes, Category, Neighborhood
            FROM Post WHERE UserID = %s
        """, (user_id,))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_received_reviews(user_id):
    """Return all reviews received by the given user."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.ReviewContent, r.TransactionSatisfaction, u.Nickname AS AuthorNickname
            FROM Review r
            JOIN users u ON r.AuthorID = u.UserID
            WHERE r.TargetID = %s
        """, (user_id,))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_user_chats(user_id):
    """Return distinct chat rooms the user is part of."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT DISTINCT PostID, ReceiverID, SenderID
            FROM Chats
            WHERE SenderID = %s OR ReceiverID = %s
        """, (user_id, user_id))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_user_transactions(user_id):
    """Return all transactions involving the given user, with review status."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                t.TransactionID, t.PostID, t.SellerID, t.BuyerID, p.Title,
                CASE
                    WHEN t.SellerID = %s THEN 'Seller'
                    WHEN t.BuyerID = %s THEN 'Buyer'
                END AS Role,
                (SELECT COUNT(*) FROM Review r
                 WHERE r.TransactionID = t.TransactionID AND r.AuthorID = %s) AS ReviewExists
            FROM Transactions t
            JOIN Post p ON t.PostID = p.PostID
            WHERE t.SellerID = %s OR t.BuyerID = %s
        """, (user_id, user_id, user_id, user_id, user_id))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Chat queries
# ---------------------------------------------------------------------------

def get_chat_messages(post_id, user1_id, user2_id):
    """Return all messages in a chat thread between two users on a post."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.Message, c.Timestamp, s.Nickname AS SenderNickname
            FROM Chats c
            JOIN users s ON c.SenderID = s.UserID
            WHERE c.PostID = %s
              AND ((c.SenderID = %s AND c.ReceiverID = %s)
                   OR (c.SenderID = %s AND c.ReceiverID = %s))
            ORDER BY c.Timestamp
        """, (post_id, user1_id, user2_id, user2_id, user1_id))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_chat_message(sender_id, receiver_id, post_id, message):
    """Insert a new chat message."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Chats (SenderID, ReceiverID, PostID, Message)
            VALUES (%s, %s, %s, %s)
        """, (sender_id, receiver_id, post_id, message))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Review queries
# ---------------------------------------------------------------------------

def insert_review(transaction_id, author_id, target_id, post_id, satisfaction, content):
    """Insert a review and update the target user's TransactionSatisfaction atomically.
    Raises ValueError if a review already exists for this transaction+author.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check for duplicate review
        cursor.execute("""
            SELECT COUNT(*) AS cnt FROM Review
            WHERE TransactionID = %s AND AuthorID = %s
        """, (transaction_id, author_id))
        if cursor.fetchone()["cnt"] > 0:
            raise ValueError("You have already submitted a review for this transaction.")

        # Insert review
        cursor.execute("""
            INSERT INTO Review (TransactionID, AuthorID, TargetID, PostID, TransactionSatisfaction, ReviewContent)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (transaction_id, author_id, target_id, post_id, satisfaction, content))

        # Update target user's satisfaction
        cursor.execute("""
            SELECT TransactionSatisfaction, TotalReviews FROM users WHERE UserID = %s
        """, (target_id,))
        user = cursor.fetchone()
        if not user:
            raise Exception(f"User {target_id} not found.")

        current = float(user["TransactionSatisfaction"])
        total = user["TotalReviews"]
        updated = round(((current * total) + satisfaction) / (total + 1), 1)

        cursor.execute("""
            UPDATE users SET TransactionSatisfaction = %s, TotalReviews = TotalReviews + 1
            WHERE UserID = %s
        """, (updated, target_id))

        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
