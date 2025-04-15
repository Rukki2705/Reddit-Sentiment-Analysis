# dashboard.py

import streamlit as st
import pandas as pd
import mysql.connector

# ✅ Set page configuration FIRST
st.set_page_config(page_title="Reddit Sentiment Dashboard", layout="wide")

# ────────────────────────────────────────
# 🔧 MySQL Connection Settings
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'  # change if needed
MYSQL_PASSWORD = ''  # change to your actual password
MYSQL_DATABASE = 'reddit_sentiment'

# ────────────────────────────────────────
# 📥 Load and clean data from MySQL
@st.cache_data(ttl=600)
def load_data():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    query = """
        SELECT subreddit, post_title, comment_body, sentiment, sentiment_score, created_utc, fetched_at
        FROM reddit_comments_sentiment
        ORDER BY fetched_at DESC;
    """
    df = pd.read_sql(query, connection)
    connection.close()

    # ✅ Normalize subreddit names for reliable filtering
    df['subreddit'] = df['subreddit'].astype(str).str.lower().str.strip()
    return df

# ────────────────────────────────────────
# 🎯 Load Data
df = load_data()

# ────────────────────────────────────────
# 🎯 Title & Filters
st.title("📈 Reddit Sentiment Analysis Dashboard")
st.caption("Live Reddit comments streamed via Kafka → analyzed with VADER → stored in MySQL")

# ✅ Subreddit Dropdown
subreddits = sorted(df['subreddit'].dropna().unique())
selected_subreddit = st.selectbox("🎯 Filter by Subreddit", ['All'] + subreddits)

# Filter data by selected subreddit
if selected_subreddit != 'All':
    df = df[df['subreddit'] == selected_subreddit]

# ────────────────────────────────────────
# 📊 Sentiment Distribution Chart
st.subheader("📊 Sentiment Distribution")
sentiment_counts = df['sentiment'].value_counts()
st.bar_chart(sentiment_counts)

# ────────────────────────────────────────
# 📰 Latest Comments Table
st.subheader("📰 Latest Reddit Comments")
st.dataframe(
    df[['subreddit', 'comment_body', 'sentiment', 'sentiment_score', 'fetched_at']].head(20),
    use_container_width=True
)

# ────────────────────────────────────────
# 🌟 Top 5 Positive Comments
st.subheader("🌟 Top 5 Positive Comments")
top_positive = df[df['sentiment'] == 'positive'].sort_values(by='sentiment_score', ascending=False).head(5)

for _, row in top_positive.iterrows():
    with st.container():
        st.markdown(f"**Subreddit:** r/{row['subreddit']}")
        st.markdown(f"**Sentiment Score:** `{row['sentiment_score']:.4f}`")
        st.markdown("**Comment:**")
        st.markdown(f"> {row['comment_body']}")
        st.markdown("---")

# ────────────────────────────────────────
# ⚡ Top 5 Negative Comments
st.subheader("⚡ Top 5 Negative Comments")
top_negative = df[df['sentiment'] == 'negative'].sort_values(by='sentiment_score').head(5)

for _, row in top_negative.iterrows():
    with st.container():
        st.markdown(f"**Subreddit:** r/{row['subreddit']}")
        st.markdown(f"**Sentiment Score:** `{row['sentiment_score']:.4f}`")
        st.markdown("**Comment:**")
        st.markdown(f"> {row['comment_body']}")
        st.markdown("---")
