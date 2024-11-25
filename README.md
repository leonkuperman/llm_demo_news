LLM Demo News

Overview

LLM Demo News is a demonstration project showcasing the integration of financial news sentiment analysis using a Large Language Model (LLM). This project fetches market-related news articles, classifies their sentiment (positive, negative, neutral), and categorizes them by industry (e.g., Technology, Healthcare, etc.). It includes a backend powered by FastAPI and a React-based frontend for real-time visualization.

Features
•	News Fetching: Retrieves market news from Finnhub.
•	Sentiment Analysis: Uses an LLM to classify article sentiment from -5 (negative) to 5 (positive).
•	Industry Categorization: Assigns articles to specific industries based on content.
•	Real-Time Dashboard: Displays a timeline of sentiment scores and categorized articles in a browser-based UI.

Tech Stack
•	Backend: FastAPI, Python
•	Frontend: React, Chart.js
•	Database: SQLite
•	LLM Integration: Local endpoint for LLM (compatible with OpenAI APIs)
•	APIs:
•	Finnhub API for news data
•	Custom LLM API for sentiment analysis