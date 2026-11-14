
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


from fastapi import FastAPI, Query
from app.database import get_connection
import math
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.run_database_pipeline import run_pipeline



logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("newsgen.scheduler")

scheduler = BackgroundScheduler(
    timezone="Asia/Kolkata"
)


def scheduled_news_job():
    logger.info("Starting scheduled RSS news collection...")

    try:
        result = run_pipeline()
        logger.info("Scheduled pipeline completed: %s", result)

    except RuntimeError as error:
        logger.warning("Pipeline was skipped: %s", error)

    except Exception:
        logger.exception("Scheduled RSS pipeline failed")


ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):

    if ENABLE_SCHEDULER:
        logger.info("Starting NewsGen AI scheduler...")

        scheduler.add_job(
            scheduled_news_job,
            trigger=IntervalTrigger(hours=10),
            id="newsgen_rss_job",
            name="Automatic RSS News Fetching",
            max_instances=1,
            coalesce=True,
            next_run_time=datetime.now(scheduler.timezone),
            replace_existing=True,
        )

        scheduler.start()
    else:
        logger.info("NewsGen AI scheduler is disabled.")

    yield

    if scheduler.running:
        logger.info("Stopping NewsGen AI scheduler...")
        scheduler.shutdown(wait=False)

app = FastAPI(
    title="NewsGen AI",
    description="AI-powered Daily News Summarizer API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to NewsGen AI API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }



@app.get("/api/articles")
def get_articles(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    offset = (page - 1) * limit

    with get_connection() as connection:

        total_articles = connection.execute(
            "SELECT COUNT(*) FROM articles"
        ).fetchone()[0]

        rows = connection.execute(
            """
            SELECT
                a.id,
                a.title,
                a.description,
                a.url,
                a.source,
                a.published,
                a.status,
                s.headline,
                s.category,
                s.summary_text
            FROM articles a
            LEFT JOIN summaries s
                ON a.id = s.article_id
            ORDER BY a.id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        ).fetchall()

        total_pages = math.ceil(total_articles / limit)

        return {
            "page": page,
            "limit": limit,
            "total_articles": total_articles,
            "total_pages": total_pages,
            "articles": [dict(row) for row in rows]
        }




@app.get("/api/articles/category/{category}")
def get_articles_by_category(category: str):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                a.id,
                a.title,
                a.source,
                a.published,
                s.headline,
                s.category,
                s.summary_text
            FROM articles a
            JOIN summaries s
                ON a.id = s.article_id
            WHERE LOWER(s.category) = LOWER(?)
            ORDER BY a.id ASC
            """,
            (category,)
        ).fetchall()

        return {
            "category": category,
            "total_articles": len(rows),
            "articles": [dict(row) for row in rows]
        }


@app.get("/api/articles/search")
def search_articles(keyword: str):
    search_term = f"%{keyword}%"

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                a.id,
                a.title,
                a.source,
                a.published,
                s.headline,
                s.category,
                s.summary_text
            FROM articles a
            LEFT JOIN summaries s
                ON a.id = s.article_id
            WHERE
                a.title LIKE ?
                OR s.headline LIKE ?
                OR s.summary_text LIKE ?
            ORDER BY a.id DESC
            """,
            (search_term, search_term, search_term)
        ).fetchall()

        return {
            "keyword": keyword,
            "total_results": len(rows),
            "articles": [dict(row) for row in rows]
        }


@app.get("/api/articles/latest")
def get_latest_articles(limit: int = Query(default=5, ge=1, le=50)):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                a.id,
                a.title,
                a.source,
                a.published,
                s.headline,
                s.category,
                s.summary_text
            FROM articles a
            LEFT JOIN summaries s
                ON a.id = s.article_id
            ORDER BY a.published DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        return {
            "total_articles": len(rows),
            "articles": [dict(row) for row in rows]
        }




@app.get("/api/categories")
def get_categories():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT DISTINCT category
            FROM summaries
            WHERE category IS NOT NULL
              AND TRIM(category) != ''
            ORDER BY category ASC
            """
        ).fetchall()

        categories = [row["category"] for row in rows]

        return {
            "total_categories": len(categories),
            "categories": categories
        }


@app.get("/api/dashboard/stats")
def get_dashboard_stats():
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

        total_categories = connection.execute(
            "SELECT COUNT(DISTINCT category) FROM summaries"
        ).fetchone()[0]

        return {
            "total_articles": total_articles,
            "total_summaries": total_summaries,
            "pending_articles": pending_articles,
            "failed_articles": failed_articles,
            "total_categories": total_categories
        }

@app.post("/api/rss/refresh")
def manual_rss_refresh():

    try:
        result = run_pipeline()

        return {
            "message": "RSS pipeline completed successfully",
            "result": result
        }

    except RuntimeError as error:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    except Exception as error:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
