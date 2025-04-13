from flask import Flask, request, jsonify
from flask_cors import CORS
from src.scrapers.reddit_scraper import scrape_reddit
from src.scrapers.hackernews_scraper import scrape_hackernews
from src.scrapers.quora_scraper import scrape_quora
from src.analyzers.sentiment_analyzer import analyze_sentiment
from src.analyzers.keyword_extractor import extract_keywords
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    project = data.get('project', '')
    platforms = data.get('platforms', [])
    num_posts = data.get('num_posts', 10)
    
    results = []
    
    if "reddit" in platforms:
        try:
            reddit_data = scrape_reddit(project, num_posts)
            for item in reddit_data:
                item['platform'] = 'Reddit'
                results.append(item)
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
    
    if "hackernews" in platforms:
        try:
            hackernews_data = scrape_hackernews(num_posts)
            for item in hackernews_data:
                item['platform'] = 'Hacker News'
                results.append(item)
        except Exception as e:
            print(f"Error scraping Hacker News: {e}")
    
    if "quora" in platforms:
        try:
            quora_data = scrape_quora(project.replace(" ", "-"), num_posts)
            for item in quora_data:
                item['platform'] = 'Quora'
                results.append(item)
        except Exception as e:
            print(f"Error scraping Quora: {e}")
    
    # Analyze sentiment and extract keywords
    for item in results:
        text = item.get("text", "") + " ".join(item.get("comments", []))
        item['sentiment'] = analyze_sentiment(text)
        item['keywords'] = extract_keywords(text)[:10]  # Limit to top 10 keywords
    
    # Calculate summary statistics
    platform_stats = {}
    for platform in platforms:
        platform_items = [item for item in results if item['platform'].lower() == platform.lower()]
        if platform_items:
            positive = sum(1 for item in platform_items if item['sentiment'] == 'Positive')
            negative = sum(1 for item in platform_items if item['sentiment'] == 'Negative')
            neutral = sum(1 for item in platform_items if item['sentiment'] == 'Neutral')
            total = len(platform_items)
            
            platform_stats[platform] = {
                'positive_percentage': (positive / total) * 100 if total > 0 else 0,
                'negative_percentage': (negative / total) * 100 if total > 0 else 0,
                'neutral_percentage': (neutral / total) * 100 if total > 0 else 0,
                'count': total
            }
    
    # Get overall sentiment
    all_sentiments = [item['sentiment'] for item in results]
    positive_count = all_sentiments.count('Positive')
    negative_count = all_sentiments.count('Negative')
    neutral_count = all_sentiments.count('Neutral')
    total_count = len(all_sentiments)
    
    overall_sentiment = {
        'positive_percentage': (positive_count / total_count) * 100 if total_count > 0 else 0,
        'negative_percentage': (negative_count / total_count) * 100 if total_count > 0 else 0,
        'neutral_percentage': (neutral_count / total_count) * 100 if total_count > 0 else 0
    }
    
    # Get top keywords across all platforms
    all_keywords = []
    for item in results:
        all_keywords.extend(item.get('keywords', []))
    
    keyword_count = {}
    for keyword in all_keywords:
        if keyword in keyword_count:
            keyword_count[keyword] += 1
        else:
            keyword_count[keyword] = 1
    
    top_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:15]
    
    response = {
        'project': project,
        'results': results,
        'platform_stats': platform_stats,
        'overall_sentiment': overall_sentiment,
        'top_keywords': [{'keyword': k, 'count': v} for k, v in top_keywords]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
