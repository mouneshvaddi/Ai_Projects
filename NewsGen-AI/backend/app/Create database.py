
import sqlite3
import hashlib
import re

from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


# Database location
DATABASE_PATH = "data/newsgen.db"


# -------------------------------------------------
# STEP 1: Database connection
# -------------------------------------------------

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# -------------------------------------------------
# STEP 2: Generate a normalized URL
# -------------------------------------------------

def normalize_url(url):

    if not url:
        return ""

    parts = urlsplit(url.strip())

    # Remove tracking parameters
    query_params = [
        (key, value)
        for key, value in parse_qsl(parts.query)
        if not key.lower().startswith("utm_")
        and key.lower() not in ["fbclid", "gclid"]
    ]

    normalized = urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path.rstrip("/"),
        urlencode(query_params),
        ""
    ))

    return normalized


# -------------------------------------------------
# STEP 3: Generate unique article hash
# -------------------------------------------------

def generate_article_hash(url):

    normalized_url = normalize_url(url)

    return hashlib.sha256(
        normalized_url.encode("utf-8")
    ).hexdigest()


# -------------------------------------------------
# STEP 4: Create database tables
# -------------------------------------------------

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


# -------------------------------------------------
# STEP 5: Start execution history
# -------------------------------------------------

def start_processing_run():

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO processing_history (started_at)
            VALUES (?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
            )
        )

        return cursor.lastrowid


# -------------------------------------------------
# STEP 6: Insert article if it is new
# -------------------------------------------------

def save_article(article):

    article_hash = generate_article_hash(
        article["link"]
    )

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO articles
            (
                title,
                description,
                url,
                url_hash,
                source,
                published,
                status
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

        if cursor.rowcount == 0:
            return None

        return cursor.lastrowid


# -------------------------------------------------
# STEP 7: Get article ID
# -------------------------------------------------

def get_article_id(url):

    article_hash = generate_article_hash(url)

    with get_connection() as connection:

        result = connection.execute(
            """
            SELECT id
            FROM articles
            WHERE url_hash = ?
            """,
            (article_hash,)
        ).fetchone()

        return result["id"] if result else None


# -------------------------------------------------
# STEP 8: Save AI summary
# -------------------------------------------------

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

    headline = (
        headline_match.group(1).strip()
        if headline_match else ""
    )

    category = (
        category_match.group(1).strip()
        if category_match else "Other"
    )

    with get_connection() as connection:

        connection.execute(
            """
            INSERT OR REPLACE INTO summaries
            (
                article_id,
                headline,
                category,
                summary_text
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                article_id,
                headline,
                category,
                summary_text
            )
        )

        connection.execute(
            """
            UPDATE articles
            SET status = 'completed'
            WHERE id = ?
            """,
            (article_id,)
        )


# -------------------------------------------------
# STEP 9: Update article status
# -------------------------------------------------

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


# -------------------------------------------------
# STEP 10: Complete processing history
# -------------------------------------------------

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


# -------------------------------------------------
# STEP 11: Display database statistics
# -------------------------------------------------

def show_database_statistics():

    with get_connection() as connection:

        total_articles = connection.execute(
            "SELECT COUNT(*) FROM articles"
        ).fetchone()[0]

        total_summaries = connection.execute(
            "SELECT COUNT(*) FROM summaries"
        ).fetchone()[0]

        pending_articles = connection.execute(
            "SELECT COUNT(*) FROM articles WHERE status = 'pending'"
        ).fetchone()[0]

        failed_articles = connection.execute(
            "SELECT COUNT(*) FROM articles WHERE status = 'failed'"
        ).fetchone()[0]

    print("\nDATABASE STATISTICS")
    print("-" * 40)

    print(f"Total articles: {total_articles}")
    print(f"Total summaries: {total_summaries}")
    print(f"Pending articles: {pending_articles}")
    print(f"Failed articles: {failed_articles}")
