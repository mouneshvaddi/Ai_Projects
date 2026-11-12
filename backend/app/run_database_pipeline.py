
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
    # Supports: python app/run_database_pipeline.py
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


# Prevent scheduled and manual executions from overlapping.
pipeline_lock = threading.Lock()


def run_pipeline():
    if not pipeline_lock.acquire(blocking=False):
        raise RuntimeError("News pipeline is already running.")

    try:
        print("\n" + "=" * 60)
        print("NEWSGEN AI - AUTOMATIC RSS PIPELINE")
        print("=" * 60)

        initialize_database()
        run_id = start_processing_run()

        fetched_count = 0
        new_count = 0
        duplicate_count = 0
        summarized_count = 0
        failed_count = 0

        try:
            # STEP 1: Fetch RSS articles
            articles = fetch_all_news()
            fetched_count = len(articles)

            # STEP 2: Remove duplicate URLs
            unique_articles = remove_duplicates(articles)

            print(f"\nFetched articles: {fetched_count}")
            print(f"Unique articles: {len(unique_articles)}")

            # STEP 3: Save new articles
            for article in unique_articles:
                article_id = save_article(article)

                if article_id is not None:
                    new_count += 1

            duplicate_count = len(unique_articles) - new_count

            print(f"New articles saved: {new_count}")
            print(f"Existing articles skipped: {duplicate_count}")

            # STEP 4: Retrieve all pending articles
            pending_articles = get_pending_articles()

            print(
                f"\nArticles waiting for summarization: "
                f"{len(pending_articles)}"
            )

            # STEP 5: Summarize pending articles
            for index, article in enumerate(
                pending_articles, start=1
            ):
                article_id = article["id"]

                print(
                    f"\nPROCESSING ARTICLE "
                    f"{index}/{len(pending_articles)}"
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

            # STEP 6: Save processing history
            complete_processing_run(
                run_id=run_id,
                fetched=fetched_count,
                new_articles=new_count,
                duplicates=duplicate_count,
                summarized=summarized_count,
                failed=failed_count,
            )

        except Exception as error:
            print(f"Pipeline error: {error}")

            complete_processing_run(
                run_id=run_id,
                fetched=fetched_count,
                new_articles=new_count,
                duplicates=duplicate_count,
                summarized=summarized_count,
                failed=failed_count,
            )
            raise

        show_database_statistics()

        result = {
            "status": "completed",
            "fetched": fetched_count,
            "new_articles": new_count,
            "duplicates": duplicate_count,
            "summarized": summarized_count,
            "failed": failed_count,
        }

        print("\nNEWSGEN AI PIPELINE COMPLETED")
        print(result)

        return result

    finally:
        pipeline_lock.release()


def main():
    return run_pipeline()


if __name__ == "__main__":
    main()
