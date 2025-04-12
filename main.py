import argparse
from src.scrapers.reddit_scraper import scrape_reddit
from src.scrapers.hackernews_scraper import scrape_hackernews
from src.scrapers.quora_scraper import scrape_quora
from src.analyzers.sentiment_analyzer import analyze_sentiment
from src.analyzers.keyword_extractor import extract_keywords

def main(project, platforms):
    data = []
    
    if "reddit" in platforms:
        reddit_data = scrape_reddit("learnpython", 10)
        data.extend(reddit_data)
    
    if "hackernews" in platforms:
        hackernews_data = scrape_hackernews(10)
        data.extend(hackernews_data)
    
    if "quora" in platforms:
        quora_data = scrape_quora("python-programming", 10)
        data.extend(quora_data)
    
    # Analyze sentiment and extract keywords
    sentiment_scores = []
    keywords = []
    for item in data:
        text = item.get("text", "") + " ".join(item.get("comments", []))
        sentiment = analyze_sentiment(text)
        sentiment_scores.append(sentiment)
        keywords.extend(extract_keywords(text))
    
    # Output summary
    summary = {
        "project": project,
        "sentiment_score": sentiment_scores.count("Positive") / len(sentiment_scores),
        "top_keywords": keywords,
        "highlights": ["Example highlight"]
    }
    
    print(summary)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Market Research Bot')
    parser.add_argument('--project', type=str, help='Project name')
    parser.add_argument('--platforms', type=str, nargs='+', help='Platforms to scrape')
    args = parser.parse_args()
    
    main(args.project, args.platforms)
