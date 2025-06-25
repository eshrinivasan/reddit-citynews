import os
import praw

# Set your Reddit API credentials here or use environment variables
REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID', 'YOUR_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET', 'YOUR_CLIENT_SECRET')
REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT', 'traffic-app/0.1 by YOUR_USERNAME')

TRAFFIC_KEYWORDS = [
    'traffic', 'jam', 'accident', 'signal', 'congestion', 'roadblock', 'slow', 'block', 'diversion', 'closed', 'delay', 'pileup', 'crash', 'snarl', 'bottleneck', 'police', 'road work', 'construction'
]

AREA_KEYWORDS = [
    'outer ring road', 'orr', 'marathahalli', 'whitefield', 'sarjapur', 'bellandur', 'mahadevapura', 'kadubeesanahalli', 'kr puram', 'kundalahalli', 'brookefield', 'itpl', 'varthur', 'hebbal', 'tin factory'
]

def fetch_traffic_posts(subreddit_names=None, limit=30):
    if subreddit_names is None:
        subreddit_names = ['bangalore', 'bangalore_traffic', 'BangaloreTravel', 'BangaloreInsta', 'BangaloreStartups']
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = []
    from datetime import datetime
    for sub_name in subreddit_names:
        try:
            subreddit = reddit.subreddit(sub_name)
            for submission in subreddit.new(limit=limit):
                title_lower = submission.title.lower()
                # Show posts that mention either a traffic keyword or an area keyword
                if any(keyword in title_lower for keyword in TRAFFIC_KEYWORDS + AREA_KEYWORDS):
                    # Remove all keyword highlighting
                    body = submission.selftext or ''
                    posts.append({
                        'title': submission.title,
                        'body': body[:500] + ('...' if len(body) > 500 else ''),
                        'url': submission.url if submission.url.startswith('http') else f"https://reddit.com{submission.permalink}",
                        'author': submission.author.name if submission.author else 'unknown',
                        'created': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M'),
                        'subreddit': sub_name
                    })
        except Exception as e:
            continue
    # Sort by most recent
    posts.sort(key=lambda x: x['created'], reverse=True)
    return posts

# Add a note for Streamlit users:
if __name__ == '__main__':
    print("This script is intended to be used with Streamlit. Please run: streamlit run reddit_traffic.py")
