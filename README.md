# Reddit-Sentiment-Analysis

A real-time sentiment analysis project that streams Reddit comments using Kafka, analyzes them with VADER, stores results in MySQL, and visualizes insights on a Streamlit dashboard.

---

## 🧩 Features

- 🔄 Real-time comment ingestion from multiple subreddits using Kafka
- 🧠 Sentiment analysis using VADER (positive / neutral / negative)
- 🗄️ Persistent storage in MySQL for historical tracking
- 📊 Streamlit-based interactive dashboard to explore subreddit-specific sentiments

---

## 🛠️ Tech Stack

| Layer         | Technology                      |
|--------------|----------------------------------|
| Ingestion     | Reddit API + Kafka Producer     |
| Processing    | Kafka Consumer + VADER (NLP)    |
| Storage       | MySQL                           |
| Visualization | Streamlit Dashboard             |

---

## ⚙️ Kafka Setup (Windows)

### Start Zookeeper

```bash
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

### Start Kafka Broker
```bash
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

# Create a Topic
```bash
.\bin\windows\kafka-topics.bat --create --topic reddit-comments --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
---
## 📦 Setup Instructions

1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

2️⃣ Start Services
Ensure Kafka, Zookeeper, and MySQL are running 


3️⃣ Run the Kafka Producer
```bash
python kafka_producer.py
```

4️⃣ Run the Kafka Consumer
```bash
python kafka-consumer.py
```

5️⃣ Launch the Streamlit Dashboard
```bash
streamlit run dashboard.py
```
---

## 🧪 Sample Output
#### ✅ Top 5 positive & negative comments

#### 📉 Bar chart of sentiment distribution

#### 📰 Data table of latest comments
