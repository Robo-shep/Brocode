import praw
from praw.models import Submission
from praw.models import Comment

# Reddit API credentials
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "your_user_agent"

def scrape_reddit(subreddit_name, num_posts):
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent=REDDIT_USER_AGENT)
    
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=num_posts)
    
    data = []
    for post in posts:
        post_data = {
            "title": post.title,
            "text": post.selftext,
            "comments": []
        }
        
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            post_data["comments"].append(comment.body)
        
        data.append(post_data)
    
    return data

# Example usage
if __name__ == "__main__":
    subreddit_name = "learnpython"
    num_posts = 10
    reddit_data = scrape_reddit(subreddit_name, num_posts)
    print(reddit_data)
