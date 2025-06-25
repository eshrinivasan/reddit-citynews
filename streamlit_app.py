import streamlit as st
from reddit_traffic import fetch_traffic_posts
import os

st.set_page_config(page_title="Bangalore Traffic Updates", layout="centered")

# Inject CSS to adjust top padding/margin and highlight subreddit name
st.markdown("""
    <style>
        .main .block-container { padding-top: 0.1rem !important; }
        header { margin-bottom: 0 !important; }
        h1 { margin-top: 0 !important; font-size: 2.1rem !important; }
        .st-emotion-cache-1w723zb { padding-top: 0.1rem !important; }
        .subreddit-highlight { background: #ffe066; color: #222; border-radius: 3px; padding: 0 4px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.title("🚦 Bangalore Traffic Updates")

# Use Streamlit tabs for source selection
reddit_tab, twitter_tab = st.tabs(["Reddit", "Twitter"])

with reddit_tab:
    posts = fetch_traffic_posts()
    if posts:
        for post in posts:
            st.markdown(f"**[{post['title']}]({post['url']})**  ", unsafe_allow_html=True)
            st.markdown(f"*Posted by {post['author']} in <span class='subreddit-highlight'>r/{post['subreddit']}</span> at {post['created']}*", unsafe_allow_html=True)
            if post['body']:
                st.write(post['body'])
            st.markdown('<hr style="margin:8px 0; border:0; border-top:1px solid #eee;" />', unsafe_allow_html=True)
    else:
        st.write("No recent traffic-related posts found.")

with twitter_tab:
    #st.info("Twitter API access requires credentials and may be rate-limited or paid. Please configure your Twitter API keys in the environment.")
    import tweepy
    TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN', '')
    TRAFFIC_KEYWORDS = [
        'traffic', 'jam', 'accident', 'signal', 'congestion', 'roadblock', 'slow', 'block', 'diversion', 'closed', 'delay', 'pileup', 'crash', 'snarl', 'bottleneck', 'police', 'road work', 'construction',
        'outer ring road', 'orr', 'marathahalli', 'whitefield', 'sarjapur', 'bellandur', 'mahadevapura', 'kadubeesanahalli', 'kr puram', 'kundalahalli', 'brookefield', 'itpl', 'varthur', 'hebbal', 'tin factory', 'bangalore'
    ]
    def fetch_twitter_traffic(query="bangalore traffic", max_results=20):
        if not TWITTER_BEARER_TOKEN or TWITTER_BEARER_TOKEN.strip() == "":
            st.warning("Twitter Bearer Token is not set or is empty. Please check your environment variable TWITTER_BEARER_TOKEN.")
            return []
        client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)
        tweets = []
        try:
            response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "author_id", "text"])
            for tweet in response.data or []:
                text_lower = tweet.text.lower()
                if any(keyword in text_lower for keyword in TRAFFIC_KEYWORDS):
                    tweets.append({
                        'text': tweet.text,
                        'created': tweet.created_at.strftime('%Y-%m-%d %H:%M'),
                        'author_id': tweet.author_id
                    })
        except Exception as e:
            st.error(f"Error fetching tweets: {e}")
        return tweets
    tweets = fetch_twitter_traffic()
    if tweets:
        for tweet in tweets:
            st.markdown(f"**{tweet['text']}**")
            st.markdown(f"*Posted by user {tweet['author_id']} at {tweet['created']}*")
            st.markdown('<hr style="margin:8px 0; border:0; border-top:1px solid #eee;" />', unsafe_allow_html=True)
    else:
        st.write("No recent traffic-related tweets found or Twitter API not configured.")
