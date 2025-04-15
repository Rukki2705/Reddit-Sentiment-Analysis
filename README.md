# Reddit-Sentiment-Analysis

.\bin\windows\zookeeper-server-start.bat .\config\zookeeeper.properties

.\bin\windows\kafka-server-start.bat .\config\server.properties


.\bin\windows\kafka-topics.bat --create --topic reddit-comments --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
