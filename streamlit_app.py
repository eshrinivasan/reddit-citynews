import streamlit as st
from reddit_traffic import fetch_traffic_posts

st.title("🚦 Bangalore Traffic Updates (Reddit)")
posts = fetch_traffic_posts()
if posts:
    for post in posts:
        st.markdown(f"**[{post['title']}]({post['url']})**  ")
        st.markdown(f"*Posted by {post['author']} in r/{post['subreddit']} at {post['created']}*")
        if post['body']:
            st.write(post['body'])
        st.markdown("---")
else:
    st.write("No recent traffic-related posts found.")
