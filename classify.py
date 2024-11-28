import requests
import json
from db_setup import get_db_connection
import logging
import time
from openai import OpenAI
import main

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_prompt(article):
    # Convert Row object to dictionary
    article_dict = dict(article)
    return_prompt = """
    You are a news analyst for a financial news company. Please analyze the following news article and provide:
    - A sentiment score from -5 (negative) to 5 (positive) with 0 being completely neutral.
    - The company category if any specific company is mentioned.
    Return the response in JSON format with keys `sentiment_score` and `company_category`. 
    If no specific company is referenced, set `company_category` to `null`. When in doubt, provide
    a neutral to slightly optimistic sentiment score.

    Here is the JSON format to return with some example values:
    {
        "sentiment_score": 3,
        "company_category": "Technology",
        "company_ticker": "AAPL",
        "reasoning": "The article mentions a new product launch which is expected to drive revenue growth."
    }

    Return the JSON directly in the response, do not add any formatations. Don't return any other characters outside of the JSON response. Your response needs to be parsed programmatically.

    Article:""" + json.dumps(article_dict)
    
    logging.info(f"Formatted prompt for article {article['id']}: {return_prompt}")
    return return_prompt

def classify_articles(n=1, llm_url=None, llm_api_key=None):
    client = OpenAI(
        base_url=llm_url,
        api_key=llm_api_key
    )

    with get_db_connection() as conn:
        # Retrieve unclassified articles
        sql_query = """SELECT id, category, datetime, headline, image, related, 
        source, summary, url FROM articles WHERE is_classified = 0 LIMIT ?"""
        cursor = conn.execute(sql_query, (n,))
        articles = cursor.fetchall()

        if not articles:
            logger.info("No unclassified articles found.")
            return

        for article in articles:
            if not main.is_classifying:
                return

            try:
                sentiment_score, company_category = classify_article(article, client)

                update_article_classification(conn, article['id'], sentiment_score, company_category)

                # Small delay to avoid rate-limiting
                #time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error classifying article {article['id']}: {e}")


def update_article_classification(conn, article_id, sentiment_score, company_category):
    try:
        conn.execute(
            '''UPDATE articles
                SET is_classified = 1,
                    market_sentiment = ?,
                    industry_category = ?
                WHERE id = ?''',
            (sentiment_score, company_category, article_id)
        )
        conn.commit()
        logger.info(f"Article {article_id} classified successfully.")
    except Exception as e:
        logger.error(f"Error updating article {article_id} classification: {e}")


def classify_article(article, client):
    prompt = format_prompt(article)
    article_id = article['id']

    chat_completion = client.chat.completions.create(
    messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model='gpt-4o-2024-05-13'
    )

    # Parse the response assuming it’s in JSON format

    # Access the completion content
    completion_content = chat_completion.choices[0].message.content
    logger.info(f"Classification response for article ID {article_id}: {completion_content}")

    # Parse the JSON content
    classification = json.loads(completion_content)

    # Extract classification data
    sentiment_score = classification.get("sentiment_score", 0)
    company_category = classification.get("company_category", "None")

    return sentiment_score, company_category

# Main function to test classification
if __name__ == '__main__':
    classify_articles(10)
    logger.info('Article classification complete.')