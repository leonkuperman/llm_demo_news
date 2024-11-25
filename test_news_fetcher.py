import unittest
import asyncio
from db_setup import get_db_connection, init_db, get_last_id
from news_fetcher import fetch_and_store_articles
from logger_config import get_logger

logger = get_logger(__name__)

class TestNewsFetcher(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()  # Initialize the test database
        logger.info("Test database initialized.")

    @classmethod
    def tearDownClass(cls):
        with get_db_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS articles")
        logger.info("Test database cleaned up.")

    def test_fetch_and_store_articles(self):
        async def run_test():
            last_id_before = get_last_id()
            
            await fetch_and_store_articles()  # Fetch and store new articles

            # Get the count of rows inserted
            with get_db_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE finnhub_id > ?", (last_id_before,))
                row_count = cursor.fetchone()[0]
            
            logger.info(f"Rows inserted during test: {row_count}")
            self.assertGreater(row_count, 0, "No new articles were inserted into the test database.")

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()