
from database import get_connection, get_pending_articles


# 1. Check database status counts
with get_connection() as connection:

    print("\nARTICLE STATUS COUNTS")

    results = connection.execute(
        """
        SELECT status, COUNT(*) AS total
        FROM articles
        GROUP BY status
        """
    ).fetchall()

    for row in results:
        print(row["status"], ":", row["total"])

    # 2. Total articles
    total = connection.execute(
        "SELECT COUNT(*) FROM articles"
    ).fetchone()[0]

    print("\nTOTAL ARTICLES:", total)

    # 3. Pending articles
    pending = connection.execute(
        """
        SELECT COUNT(*)
        FROM articles
        WHERE status = 'pending'
        """
    ).fetchone()[0]

    print("PENDING ARTICLES:", pending)


# 4. Test Python retrieval function
pending_articles = get_pending_articles()

print("\nARTICLES RETRIEVED:", len(pending_articles))

# 5. Display first five pending articles
print("\nFIRST FIVE PENDING ARTICLES:")

for article in pending_articles[:5]:

    print(
        article["id"],
        article["title"]
    )
