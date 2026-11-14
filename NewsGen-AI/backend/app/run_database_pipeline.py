from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
import threading

try:
    from .news_fetcher import fetch_all_news, remove_duplicates
    from .summarizer import summarize_article
    from .database import (
        initialize_database,
        start_processing_run,
        save_article,
        get_pending_articles,
        save_summary,
        update_article_status,
        complete_processing_run,
        show_database_statistics,
    )
except ImportError:
    from news_fetcher import fetch_all_news, remove_duplicates
    from summarizer import summarize_article
    from database import (
        initialize_database,
        start_processing_run,
        save_article,
        get_pending_articles,
        save_summary,
        update_article_status,
        complete_processing_run,
        show_database_statistics,
    )


pipeline_lock = threading.Lock()


def fetch_and_store_news():
    """Fetch RSS news and store articles without requiring Ollama."""

    if not pipeline_lock.acquire(blocking=False):
        raise RuntimeError("News pipeline is already running.")

    run_id = None

    try:
        print("\nStarting RSS news collection...")

        initialize_database()
        run_id = start_processing_run()

        articles = fetch_all_news()
        fetched_count = len(articles)

        unique_articles = remove_duplicates(articles)

        new_count = 0

        for article in unique_articles:
            article_id = save_article(article)

            if article_id is not None:
                new_count += 1

        duplicate_count = len(unique_articles) - new_count

        complete_processing_run(
            run_id=run_id,
            fetched=fetched_count,
            new_articles=new_count,
            duplicates=duplicate_count,
            summarized=0,
            failed=0,
        )

        result = {
            "status": "completed",
            "fetched": fetched_count,
            "new_articles": new_count,
            "duplicates": duplicate_count,
            "summarized": 0,
            "failed": 0,
        }

        print("RSS collection completed:", result)
        return result

    except Exception:
        if run_id is not None:
            complete_processing_run(
                run_id=run_id,
                fetched=0,
                new_articles=0,
                duplicates=0,
                summarized=0,
                failed=1,
            )
        raise

    finally:
        pipeline_lock.release()


def summarize_pending_articles():
    """Summarize pending Supabase articles using local Ollama."""

    if not pipeline_lock.acquire(blocking=False):
        raise RuntimeError("News pipeline is already running.")

    try:
        initialize_database()

        pending_articles = get_pending_articles()

        summarized_count = 0
        failed_count = 0

        print(f"Pending articles: {len(pending_articles)}")

        for index, article in enumerate(pending_articles, start=1):

            article_id = article["id"]

            print(
                f"\nPROCESSING ARTICLE {index}/{len(pending_articles)}"
            )
            print(f"Title: {article['title']}")

            try:
                summary = summarize_article(article)
                save_summary(article_id, summary)

                summarized_count += 1
                print("Status: COMPLETED")

            except Exception as error:
                failed_count += 1
                update_article_status(article_id, "failed")
                print(f"Summarization failed: {error}")

        show_database_statistics()

        return {
            "status": "completed",
            "summarized": summarized_count,
            "failed": failed_count,
        }

    finally:
        pipeline_lock.release()


def run_pipeline():
    """Run the complete pipeline locally."""

    rss_result = fetch_and_store_news()
    summary_result = summarize_pending_articles()

    return {
        **rss_result,
        "summarized": summary_result["summarized"],
        "failed": summary_result["failed"],
    }


def main():
    return run_pipeline()


if __name__ == "__main__":
    main()
