# 🕵️ Market Research Bot

A powerful Market Research Bot that scrapes, aggregates, and analyzes discourse across forums and online communities to provide insights about a specific project, product, or topic. Ideal for gauging public sentiment, identifying trends, and gathering feedback from real users.

## 🔍 Features

- Scrapes content from popular forums like Reddit, Hacker News, Quora, StackExchange, etc.
- Filters posts and comments related to a given project/topic.
- Performs sentiment analysis to gauge public opinion.
- Highlights frequently mentioned features, complaints, and suggestions.
- Summarizes the general discourse using NLP.
- (Optional) Ranks platforms by engagement or sentiment score.

## 🛠 Tech Stack

- **Backend**: Python, Flask / FastAPI
- **Web Scraping**: BeautifulSoup, Scrapy, PRAW (Reddit), API integrations
- **NLP**: spaCy, NLTK, or Hugging Face Transformers
- **Sentiment Analysis**: VADER, TextBlob, or finetuned BERT model
- **Data Storage**: MongoDB / SQLite / PostgreSQL
- **Visualization (Optional)**: Dash / Streamlit / React Frontend

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/market-research-bot.git
cd market-research-bot
```
### 2. Set up Enviornment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
### 3. Add API keys
```ini
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_agent
```
### 4. Run the BOT
```bash
python main.py --project "OpenAI GPT" --platforms reddit hackernews
```
### 5. View The Output
Check the generated summary in /outputs/summary_OpenAI_GPT.txt or as JSON in /outputs/OpenAI_GPT.json.
#### An Example Output:
```
project: "OpenAI GPT"
platforms:
  - reddit
  - hackernews
  - stackexchange
output_format: "json"
max_posts: 100

{
  "project": "OpenAI GPT",
  "sentiment_score": 0.72,
  "top_keywords": ["AI", "chatbot", "jobs", "productivity"],
  "highlights": [
    "Users are impressed by GPT's writing abilities.",
    "Concerns about misuse and ethical risks.",
    "Discussions on its impact on the job market."
  ],
  "platform_summary": {
    "Reddit": "Mixed sentiment with deeper technical discussions.",
    "Hacker News": "Focus on ethical implications and business impact."
  }
}
```
### 📦 Directory Structure
```
market-research-bot/
├── data/
│   └── raw_data/
├── outputs/
│   └── summaries/
├── src/
│   ├── scrapers/
│   ├── analyzers/
│   └── visualizer.py
├── main.py
├── config.yaml
├── requirements.txt
└── README.md
```
