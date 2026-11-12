
import os
import sqlite3
import hashlib
import re

from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


# Database configuration

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, "newsgen.db")


# 1. Database connection

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# 2. Normalize article URL

def normalize_url(url):

    parts = urlsplit(url.strip())

    query_params = [
        (key, value)
        for key, value in parse_qsl(parts.query)
        if not key.lower().startswith("utm_")
        and key.lower() not in ["fbclid", "gclid"]
    ]

    return urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path.rstrip("/"),
        urlencode(query_params),
        ""
    ))


# 3. Generate article hash

def generate_article_hash(url):

    normalized_url = normalize_url(url)

    return hashlib.sha256(
        normalized_url.encode("utf-8")
    ).hexdigest()


# 4. Initialize database

def initialize_database():

    with get_connection() as connection:

        connection.executescript("""

        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            url_hash TEXT NOT NULL UNIQUE,
            source TEXT,
            published TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER NOT NULL UNIQUE,
            headline TEXT,
            category TEXT,
            summary_text TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(article_id)
                REFERENCES articles(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS processing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            fetched_count INTEGER DEFAULT 0,
            new_articles INTEGER DEFAULT 0,
            duplicate_count INTEGER DEFAULT 0,
            summarized_count INTEGER DEFAULT 0,
            failed_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running'
        );

        """)

    print("Database initialized successfully!")


# 5. Start processing history

def start_processing_run():

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO processing_history (started_at)
            VALUES (?)
            """,
            (datetime.now(timezone.utc).isoformat(),)
        )

        return cursor.lastrowid


# 6. Save new article

def save_article(article):

    article_hash = generate_article_hash(
        article["link"]
    )

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO articles
            (
                title, description, url,
                url_hash, source, published, status
            )
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """,
            (
                article["title"],
                article.get("description", ""),
                article["link"],
                article_hash,
                article.get("source", ""),
                article.get("published", "")
            )
        )

        return cursor.lastrowid if cursor.rowcount else None


# 7. Get pending articles

def get_pending_articles():

    with get_connection() as connection:

        results = connection.execute(
            """
            SELECT *
            FROM articles
            WHERE status = 'pending'
            ORDER BY id ASC
            
            """,
            
        ).fetchall()

        return [dict(row) for row in results]


# 8. Save AI summary

def save_summary(article_id, summary_text):

    headline_match = re.search(
        r"HEADLINE:\s*(.*)",
        summary_text,
        re.IGNORECASE
    )

    category_match = re.search(
        r"CATEGORY:\s*(.*)",
        summary_text,
        re.IGNORECASE
    )

    headline = headline_match.group(1).strip() if headline_match else ""

    category = category_match.group(1).strip() if category_match else "Other"

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO summaries
            (article_id, headline, category, summary_text)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(article_id) DO UPDATE SET
                headline = excluded.headline,
                category = excluded.category,
                summary_text = excluded.summary_text
            """,
            (article_id, headline, category, summary_text)
        )

        connection.execute(
            """
            UPDATE articles
            SET status = 'completed'
            WHERE id = ?
            """,
            (article_id,)
        )


# 9. Update article status

def update_article_status(article_id, status):

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE articles
            SET status = ?
            WHERE id = ?
            """,
            (status, article_id)
        )


# 10. Complete processing history

def complete_processing_run(
    run_id,
    fetched,
    new_articles,
    duplicates,
    summarized,
    failed
):

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE processing_history
            SET completed_at = ?,
                fetched_count = ?,
                new_articles = ?,
                duplicate_count = ?,
                summarized_count = ?,
                failed_count = ?,
                status = 'completed'
            WHERE id = ?
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                fetched,
                new_articles,
                duplicates,
                summarized,
                failed,
                run_id
            )
        )


# 11. Database statistics

def show_database_statistics():

    with get_connection() as connection:

        total = connection.execute(
            "SELECT COUNT(*) FROM articles"
        ).fetchone()[0]

        summaries = connection.execute(
            "SELECT COUNT(*) FROM summaries"
        ).fetchone()[0]

        pending = connection.execute(
            "SELECT COUNT(*) FROM articles WHERE status='pending'"
        ).fetchone()[0]

        failed = connection.execute(
            "SELECT COUNT(*) FROM articles WHERE status='failed'"
        ).fetchone()[0]

    print("\nDATABASE STATISTICS")
    print("-" * 40)

    print(f"Total articles: {total}")
    print(f"Total summaries: {summaries}")
    print(f"Pending articles: {pending}")
    print(f"Failed articles: {failed}")
