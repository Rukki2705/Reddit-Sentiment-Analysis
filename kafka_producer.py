# reddit_kafka_producer.py

import praw
import json
import time
from datetime import datetime
from kafka import KafkaProducer

# Reddit API credentials
REDDIT_CLIENT_ID = 'FP95WJXPIAmtkNkxDxRxrw'
REDDIT_CLIENT_SECRET = 'LnLuhXyVs-vKrf5Xdvy4wHLCMe4I6Q'
REDDIT_USER_AGENT = 'East_Employee_8969'

# Kafka settings
KAFKA_TOPIC = 'reddit-comments'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'  # Assuming Kafka is running locally

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def stream_comments_to_kafka(subreddits, post_limit=5):
    """
    Fetch comments from hot/new posts in the given subreddits and stream them into Kafka.
    """
    print(f"Starting to stream comments from subreddits: {subreddits}")
    subreddit = reddit.subreddit(subreddits)

    # Fetch 'hot' posts
    for post in subreddit.hot(limit=post_limit):
        print(f"\n[HOT] Post Title: {post.title}")
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            comment_data = {
                'subreddit': comment.subreddit.display_name,
                'post_title': post.title,
                'comment_body': comment.body,
                'created_utc': datetime.utcfromtimestamp(comment.created_utc).isoformat(),
                'fetched_at': datetime.now().isoformat()
            }
            # Send to Kafka
            producer.send(KAFKA_TOPIC, value=comment_data)
            print(f"Sent comment from r/{comment_data['subreddit']} to Kafka.")

    # Fetch 'new' posts
    for post in subreddit.new(limit=post_limit):
        print(f"\n[NEW] Post Title: {post.title}")
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            comment_data = {
                'subreddit': comment.subreddit.display_name,
                'post_title': post.title,
                'comment_body': comment.body,
                'created_utc': datetime.utcfromtimestamp(comment.created_utc).isoformat(),
                'fetched_at': datetime.now().isoformat()
            }
            # Send to Kafka
            producer.send(KAFKA_TOPIC, value=comment_data)
            print(f"Sent comment from r/{comment_data['subreddit']} to Kafka.")

    # Flush to ensure all messages are sent
    producer.flush()

if __name__ == "__main__":
    subreddits_to_track = "technology+news+cryptocurrency+finance"

    stream_comments_to_kafka(subreddits_to_track, post_limit=3)
