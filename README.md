# 🕵️ Market Research Bot

A powerful Market Research Bot that scrapes, aggregates, and analyzes discourse across forums and online communities to provide insights about a specific project, product, or topic. Ideal for gauging public sentiment, identifying trends, and gathering feedback from real users.

## 🔍 Features

- Scrapes content from popular forums like Reddit, Hacker News, Quora, StackExchange, etc.
- Filters posts and comments related to a given project/topic.
- Performs sentiment analysis to gauge public opinion.
- Highlights frequently mentioned features, complaints, and suggestions.
- Summarizes the general discourse using NLP.
- Visualizes sentiment data and keyword trends.

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Web Scraping**: BeautifulSoup, PRAW (Reddit API)
- **NLP**: spaCy, NLTK
- **Sentiment Analysis**: VADER
- **Frontend**: HTML, CSS, JavaScript

## 🚀 Getting Started

### 1. Clone the Repository

Download the project files to your local machine.

### 2. Set up Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Configure API Keys

Edit the following files to add your API credentials:

- `src/scrapers/reddit_scraper.py`: Add your Reddit API credentials

```python
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "your_user_agent"
```

### 4. Run the Backend Server

```bash
python app.py
```

This will start the Flask server on http://localhost:5000.

### 5. Test the Application

```bash
python simple_test.py
```

This will:
- Start the Flask server in a new command window
- Run a test on the API endpoint
- Open a simple HTML frontend in your browser for testing

## 📊 Using the Application

1. Enter a search term (e.g., "Python", "AI", "Web Development")
2. Select platforms to search (Reddit, Hacker News, Quora)
3. Click "Search" to retrieve and analyze data
4. View sentiment analysis, top keywords, and sample results

## 📦 Project Structure

```
market-research-bot/
├── src/
│   ├── scrapers/
│   │   ├── reddit_scraper.py
│   │   ├── hackernews_scraper.py
│   │   └── quora_scraper.py
│   ├── analyzers/
│   │   ├── sentiment_analyzer.py
│   │   └── keyword_extractor.py
│   └── visualizer.py
├── app.py              # Flask API server
├── main.py             # Command-line interface
├── test_api.py         # API endpoint tests
├── simple_test.py      # Combined backend/frontend test
├── test_frontend.html  # Simple HTML frontend for testing
├── requirements.txt
└── README.md
```

## 📝 Future Improvements

- Add more data sources (Twitter, Product Hunt, etc.)
- Implement more advanced sentiment analysis
- Create a more sophisticated frontend with data visualizations
- Add user authentication and saved searches
- Implement caching to improve performance
