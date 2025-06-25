import os
from flask import Flask, render_template_string, request
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

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Bangalore Traffic from Reddit</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f5f6fa; margin: 0; padding: 0; }
    .container { max-width: 700px; margin: 40px auto; background: #fff; border-radius: 18px; box-shadow: 0 4px 24px 0 rgba(60,60,60,0.08); padding: 32px; }
    h2 { color: #007aff; }
    .post { margin-bottom: 22px; padding-bottom: 12px; border-bottom: 1px solid #e5e9f2; }
    .post:last-child { border-bottom: none; }
    .title { font-size: 1.1rem; font-weight: 600; color: #222; }
    .meta { color: #888; font-size: 0.95rem; }
    .subreddit { color: #007aff; font-size: 0.95rem; margin-left: 8px; }
    .body { color: #333; font-size: 1rem; margin-top: 6px; margin-bottom: 4px; }
    mark { background: #ffe066; color: #222; border-radius: 3px; padding: 0 2px; }
    a { color: #007aff; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <h2>🚦 Bangalore Traffic Updates (Reddit)</h2>
    {% if posts %}
      {% for post in posts %}
        <div class="post">
          <div class="title"><a href="{{ post['url'] }}" target="_blank">{{ post['title']|safe }}</a><span class="subreddit">[r/{{ post['subreddit'] }}]</span></div>
          <div class="meta">Posted by {{ post['author'] }} | {{ post['created'] }}</div>
          {% if post['body'] %}
            <div class="body">{{ post['body']|safe }}</div>
          {% endif %}
        </div>
      {% endfor %}
    {% else %}
      <p>No recent traffic-related posts found.</p>
    {% endif %}
  </div>
</body>
</html>
'''

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
                    highlighted_title = submission.title
                    for keyword in TRAFFIC_KEYWORDS + AREA_KEYWORDS:
                        if keyword in highlighted_title.lower():
                            highlighted_title = highlighted_title.replace(
                                keyword,
                                f'<mark>{keyword}</mark>'
                            )
                            highlighted_title = highlighted_title.replace(
                                keyword.capitalize(),
                                f'<mark>{keyword.capitalize()}</mark>'
                            )
                    # Fetch and highlight keywords in the post body (selftext)
                    body = submission.selftext or ''
                    highlighted_body = body
                    for keyword in TRAFFIC_KEYWORDS + AREA_KEYWORDS:
                        if keyword in highlighted_body.lower():
                            highlighted_body = highlighted_body.replace(
                                keyword,
                                f'<mark>{keyword}</mark>'
                            )
                            highlighted_body = highlighted_body.replace(
                                keyword.capitalize(),
                                f'<mark>{keyword.capitalize()}</mark>'
                            )
                    posts.append({
                        'title': highlighted_title,
                        'body': highlighted_body[:500] + ('...' if len(highlighted_body) > 500 else ''),
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

@app.route('/')
def index():
    posts = fetch_traffic_posts()
    return render_template_string(HTML_TEMPLATE, posts=posts)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
