
import feedparser
import requests
import re
import html
from datetime import datetime, timezone


# Step 1: Configure news sources

NEWS_SOURCES = {
    "BBC Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",

    "TechCrunch": "https://techcrunch.com/feed/",

    "The Verge": "https://www.theverge.com/rss/index.xml",

    "Hacker News": "https://hnrss.org/frontpage"
}


# Step 2: Clean HTML from article descriptions

def clean_html(text):

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)

    text = html.unescape(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Step 3: Fetch articles from one RSS source

def fetch_from_source(source_name, feed_url):

    articles = []

    try:

        print(f"\nFetching news from {source_name}...")

        response = requests.get(
            feed_url,
            headers={
                "User-Agent": "NewsGenAI/1.0"
            },
            timeout=20
        )

        response.raise_for_status()

        feed = feedparser.parse(response.content)

        if feed.bozo and not feed.entries:
            print(f"Invalid RSS feed: {source_name}")
            return articles

        for entry in feed.entries:

            title = entry.get("title", "").strip()

            link = entry.get("link", "").strip()

            description = entry.get("summary", "")

            description = clean_html(description)

            published = entry.get("published", "")

            # Convert parsed publication date to UTC
            parsed_date = (
                entry.get("published_parsed")
                or entry.get("updated_parsed")
            )

            if parsed_date:
                published = datetime(
                    *parsed_date[:6],
                    tzinfo=timezone.utc
                ).strftime("%Y-%m-%d %H:%M UTC")

            # Ignore incomplete articles
            if not title or not link:
                continue

            article = {
                "title": title,
                "description": description,
                "link": link,
                "published": published,
                "source": source_name
            }

            articles.append(article)

        print(
            f"Successfully fetched {len(articles)} articles "
            f"from {source_name}"
        )

    except requests.exceptions.RequestException as error:

        print(f"Network error in {source_name}: {error}")

    except Exception as error:

        print(f"Unexpected error in {source_name}: {error}")

    return articles


# Step 4: Fetch news from all sources

def fetch_all_news():

    all_articles = []

    for source_name, feed_url in NEWS_SOURCES.items():

        articles = fetch_from_source(
            source_name,
            feed_url
        )

        all_articles.extend(articles)

    return all_articles


# Step 5: Remove duplicate articles

def remove_duplicates(articles):

    unique_articles = []

    seen_links = set()

    for article in articles:

        link = article["link"]

        if link not in seen_links:

            seen_links.add(link)

            unique_articles.append(article)

    return unique_articles


# Step 6: Main execution

if __name__ == "__main__":

    print("=" * 60)
    print("       NEWSGEN AI - NEWS FETCHING ENGINE")
    print("=" * 60)

    # Fetch articles
    articles = fetch_all_news()

    # Remove duplicates
    unique_articles = remove_duplicates(articles)

    print("\n" + "=" * 60)
    print(f"TOTAL ARTICLES FETCHED: {len(articles)}")
    print(f"UNIQUE ARTICLES: {len(unique_articles)}")
    print("=" * 60)

    # Display first 20 articles
    for index, article in enumerate(
        unique_articles[:20],
        start=1
    ):

        print(f"\n{index}. {article['title']}")

        print(f"Source: {article['source']}")

        print(f"Published: {article['published']}")

        print(f"Description: {article['description'][:200]}")

        print(f"Link: {article['link']}")

        print("-" * 60)
