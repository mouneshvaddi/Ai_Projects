
from dotenv import load_dotenv
load_dotenv()

from app.database import (
    get_pending_articles,
    save_summary,
    get_connection
)

articles = get_pending_articles()

if not articles:
    raise RuntimeError("No pending articles found")

article = articles[0]
article_id = article["id"]

sample_summary = """
HEADLINE:
NewsGen AI Database Test Successful

SUMMARY:
The NewsGen AI application successfully connected
to its PostgreSQL database. Article storage and
retrieval are working correctly.

KEY TAKEAWAYS:
1. PostgreSQL connection is successful.
2. Article insertion works.
3. Pending article retrieval works.

CATEGORY:
Technology

WHY IT MATTERS:
This confirms the database integration is working.
It allows NewsGen AI to store and retrieve news.
"""

save_summary(article_id, sample_summary)

with get_connection() as connection:
    result = connection.execute(
        """
        SELECT a.status, s.headline, s.category
        FROM articles a
        JOIN summaries s ON a.id = s.article_id
        WHERE a.id = %s
        """,
        (article_id,)
    ).fetchone()

print("Article status:", result["status"])
print("Headline:", result["headline"])
print("Category:", result["category"])

print("SUMMARY STORAGE TEST PASSED!")
