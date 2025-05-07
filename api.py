import praw
import json
from datetime import datetime

# Load credentials (replace with your own or use dotenv)
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "fashion-trend-bot by u/yourusername"

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id="5JR4zM8LOEOgnlHVKJWurA",
    client_secret=	"ijU-kA38p6p2Mu1vpm2rtElQUr8hvA",
    user_agent="Adventurous_Tour_395"
)

# Choose subreddit and parameters
SUBREDDITS = ["femalefashionadvice", "malefashionadvice", "streetwear"]
LIMIT = 50  # Posts per subreddit

all_posts = []

for sub_name in SUBREDDITS:
    subreddit = reddit.subreddit(sub_name)
    for post in subreddit.hot(limit=LIMIT):
        if not post.stickied:
            post_data = {
                "title": post.title,
                "author": str(post.author),
                "score": post.score,
                "url": post.url,
                "created": datetime.utcfromtimestamp(post.created_utc).isoformat(),
                "subreddit": sub_name,
                "permalink": "https://reddit.com" + post.permalink
            }
            all_posts.append(post_data)

# Save to JSON
with open("fashion_reddit_data.json", "w") as f:
    json.dump(all_posts, f, indent=2)

print(f"Saved {len(all_posts)} posts to fashion_reddit_data.json")
