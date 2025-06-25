import streamlit as st
from reddit_traffic import fetch_traffic_posts

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

st.title("🚦 Bangalore Traffic Updates (Reddit)")
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
