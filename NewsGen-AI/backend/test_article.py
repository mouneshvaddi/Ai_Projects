
from dotenv import load_dotenv
load_dotenv()

from app.database import (
    initialize_database,
    save_article,
    get_pending_articles
)

initialize_database()

article = {
    "title": "NewsGen AI Database Test",
    "description": "Testing PostgreSQL article storage.",
    "link": "https://example.com/newsgen-db-test",
    "source": "NewsGen AI",
    "published": "2026-11-14"
}

article_id = save_article(article)

print("Inserted article ID:", article_id)

pending = get_pending_articles()

print("Pending articles:", len(pending))
print("Latest article:", pending[-1]["title"])

print("ARTICLE STORAGE TEST PASSED!")
