
from news_fetcher import fetch_all_news, remove_duplicates
from summarizer import summarize_article


def main():

    print("\nNEWSGEN AI - DAILY NEWS SUMMARIZER")

    # Step 1: Fetch news
    articles = fetch_all_news()

    # Step 2: Remove duplicates
    articles = remove_duplicates(articles)

    print(f"\nTotal unique articles: {len(articles)}")

    # Step 3: Initially summarize only 3 articles
    selected_articles = articles[:]

    # Step 4: Send articles to the AI model
    for index, article in enumerate(selected_articles, start=1):

        print("\n" + "=" * 70)

        print(f"ARTICLE {index}")

        print("=" * 70)

        try:

            summary = summarize_article(article)

            print("\nAI SUMMARY:")

            print(summary)

        except Exception as error:

            print(f"Summarization failed: {error}")

    print("\nNews summarization completed!")


if __name__ == "__main__":

    main()
