# 동국 중고 마켓 (Donguk Second-Hand Marketplace)

A desktop application for buying and selling second-hand goods, built with Python, Tkinter, and MySQL.

## Features

- User registration and login
- Create, edit, and delete product listings
- Search and filter posts by title, category, neighborhood, price, status, and likes
- Like / unlike posts
- Direct messaging between buyers and sellers
- Transaction recording when a post is marked as sold
- Post-transaction reviews and satisfaction ratings
- User profile with transaction history, received reviews, and chat rooms

## Requirements

- Python 3.12+
- MySQL server running on the configured host/port
- The following Python packages:

```
mysql-connector-python
Pillow
python-dotenv
bcrypt
```

Install them with:

```bash
pip install mysql-connector-python Pillow python-dotenv bcrypt
```

## Setup

1. **Configure the database connection**

   Copy `.env.example` to `.env` and fill in your values:

   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=secondhand_marketplace
   ```

2. **Create the database schema**

   Create the `secondhand_marketplace` database in MySQL and run your schema SQL to create the required tables (`users`, `Post`, `UserLikes`, `Chats`, `Transactions`, `Review`).

3. **Add image assets** *(optional)*

   Product photos are loaded from `assets/images/` relative to the project root. Place any product images there. The homepage banner image is loaded from `ui_views/other images/`.

## Running the app

```bash
python main.py
```

## Project structure

```
second_hand_marketplace/
├── db/
│   └── queries.py        # All SQL query functions
├── ui_views/
│   ├── GUI.py            # Main window and home page
│   ├── login.py          # Login screen
│   ├── signup.py         # Registration screen
│   ├── add_post.py       # Create a new listing
│   ├── search_view_post.py  # Search, view, and edit posts
│   ├── profile.py        # User profile and transaction history
│   ├── chat.py           # Direct messaging
│   └── review.py         # Leave a review after a transaction
├── config.py             # Loads DB settings from .env
├── database.py           # get_connection() factory
├── main.py               # Entry point
└── .env                  # DB credentials (not committed)
```

## Architecture

All SQL is in `db/queries.py`. UI modules in `ui_views/` call query functions and handle display — they contain no SQL. Each query function opens and closes its own connection.

Passwords are hashed with `bcrypt` before storage. Database credentials are loaded from `.env` via `config.py` and never hardcoded.
