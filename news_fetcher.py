# news_fetcher.py
import finnhub
from db_setup import get_db_connection, get_last_id
import asyncio

from logger_config import get_logger

logger = get_logger(__name__)

async def fetch_and_store_articles(finnhub_api_key):

    finnhub_client = finnhub.Client(api_key=finnhub_api_key)

    try:
        last_id = get_last_id()  # Get the latest ID from the database
        new_articles = finnhub_client.general_news('general', min_id=last_id)
        
        with get_db_connection() as conn:
            for article in new_articles:
                conn.execute('''INSERT OR IGNORE INTO articles 
                                (finnhub_id, category, datetime, headline, image, related, source, summary, url)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (article['id'], article['category'], article['datetime'], article['headline'],
                              article['image'], article['related'], article['source'], article['summary'],
                              article['url']))
            conn.commit()  # Ensure all changes are saved
            logger.info(f"Fetched and stored {len(new_articles)} new articles.")
    except Exception as e:
        logger.error(f"Error fetching or storing articles: {e}")