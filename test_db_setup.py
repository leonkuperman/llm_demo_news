import unittest
from db_setup import get_db_connection, init_db, reset_classifications
from logger_config import get_logger

logger = get_logger(__name__)

class TestDbSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the database and the articles table
        init_db()
        logger.info("Test database initialized for reset_classifications.")

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database
        with get_db_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS articles")
        logger.info("Test database cleaned up after reset_classifications.")

    def setUp(self):
        # Insert sample data with classification values set
        with get_db_connection() as conn:
            conn.execute('''INSERT INTO articles 
                            (finnhub_id, category, datetime, headline, image, related, source, summary, url, 
                             is_classified, classification, market_sentiment, industry_category)
                            VALUES 
                            (1, 'top news', 1731357174, 'Test Headline 1', 'image1.png', '', 'Source 1', 
                             'Summary 1', 'url1.com', 1, 'Technology', 3.5, 'Information Technology'),
                            (2, 'top news', 1731357175, 'Test Headline 2', 'image2.png', '', 'Source 2', 
                             'Summary 2', 'url2.com', 1, 'Finance', -2.0, 'Financials')''')
            conn.commit()

    def test_reset_classifications(self):
        # Run the reset_classifications function
        reset_classifications()
        
        # Verify that classification fields are reset to initial state
        with get_db_connection() as conn:
            cursor = conn.execute('''SELECT is_classified, classification, market_sentiment, industry_category 
                                     FROM articles''')
            rows = cursor.fetchall()
            for row in rows:
                self.assertEqual(row['is_classified'], 0, "is_classified should be reset to 0")
                self.assertIsNone(row['classification'], "classification should be reset to NULL")
                self.assertEqual(row['market_sentiment'], 0, "market_sentiment should be reset to 0")
                self.assertIsNone(row['industry_category'], "industry_category should be reset to NULL")

if __name__ == "__main__":
    unittest.main()