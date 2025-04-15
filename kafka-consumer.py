# reddit_kafka_consumer_sentiment_mysql.py

import json
import mysql.connector
from kafka import KafkaConsumer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Kafka settings
KAFKA_TOPIC = 'reddit-comments'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# MySQL settings
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'yedazala'
MYSQL_DATABASE = 'reddit_sentiment'

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='reddit-consumer-group'
)

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Connect to MySQL
db_connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
db_cursor = db_connection.cursor()

def analyze_sentiment(text):
    """
    Analyze sentiment of a text using VADER.
    Returns: positive / negative / neutral
    """
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    
    if compound >= 0.05:
        return 'positive', compound
    elif compound <= -0.05:
        return 'negative', compound
    else:
        return 'neutral', compound

def insert_into_mysql(data):
    """
    Insert comment data into MySQL table.
    """
    sql = """
    INSERT INTO reddit_comments_sentiment 
    (subreddit, post_title, comment_body, sentiment, sentiment_score, created_utc, fetched_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['subreddit'],
        data['post_title'],
        data['comment_body'],
        data['sentiment'],
        data['sentiment_score'],
        data['created_utc'],
        data['fetched_at']
    )
    db_cursor.execute(sql, values)
    db_connection.commit()

def consume_messages():
    print(f"Starting to consume messages from {KAFKA_TOPIC} and save to MySQL...\n")
    for message in consumer:
        comment_data = message.value
        comment_text = comment_data.get('comment_body', '')

        # Perform Sentiment Analysis
        sentiment, sentiment_score = analyze_sentiment(comment_text)

        # Prepare data for insertion
        db_record = {
            'subreddit': comment_data.get('subreddit'),
            'post_title': comment_data.get('post_title'),
            'comment_body': comment_text,
            'sentiment': sentiment,
            'sentiment_score':  sentiment_score,
            'created_utc': parse_datetime(comment_data.get('created_utc')),
            'fetched_at': parse_datetime(comment_data.get('fetched_at'))
        }

        # Insert into MySQL
        insert_into_mysql(db_record)

        # Display on console
        print(f"Inserted comment from r/{db_record['subreddit']} with sentiment: {sentiment}")

def parse_datetime(dt_str):
    """
    Parse ISO8601 datetime string to Python datetime object.
    """
    if dt_str:
        return datetime.fromisoformat(dt_str)
    return None

if __name__ == "__main__":
    consume_messages()
