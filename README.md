# 동국 중고 마켓 (Donguk Second-Hand Marketplace)

![mascot](ui_views/other%20images/%EB%8D%B0%EB%B2%A0%EC%84%A4%20%EC%95%84%EC%BD%94.jpg)

A desktop application for buying and selling second-hand goods, built with Python, Tkinter, and MySQL.

> **Project Note:** This repository is shared for portfolio purposes. It was originally developed as a local course project and is not intended for direct deployment.

## Features

- User registration and login
- Create, edit, and delete product listings
- Search and filter posts by title, category, neighborhood, price, status, and likes
- Like / unlike posts
- Direct messaging between buyers and sellers
- Transaction recording when a post is marked as sold
- Post-transaction reviews and satisfaction ratings
- User profile with transaction history, received reviews, and chat rooms

## Environment

- Python 3.12+
- MySQL server
- Local `.env` file for database credentials (see `.env.example`)
- Dependencies: `mysql-connector-python`, `Pillow`, `python-dotenv`, `bcrypt`

## Entry Point

```bash
python main.py
```

## Project Structure

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
