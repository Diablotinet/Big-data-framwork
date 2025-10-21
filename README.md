# 🚀 Multi-Source Real-Time Analytics System

## Architecture
- **Apache Kafka**: Message streaming platform
- **Apache Spark**: Real-time stream processing
- **MongoDB**: NoSQL storage for analytics
- **Streamlit**: Interactive 3D dashboard

## 🏗️ Installation Automatique

```bash
python setup_infrastructure.py
```

## 🚀 Démarrage Rapide

### Option 1: Script automatique
```bash
./launch_system.bat
```

### Option 2: Démarrage manuel

1. **Démarrer Zookeeper**
```bash
./scripts/start_zookeeper.bat
```

2. **Démarrer Kafka**
```bash
./scripts/start_kafka.bat
```

3. **Créer les topics**
```bash
./scripts/create_topics.bat
```

4. **Démarrer Spark**
```bash
./scripts/start_spark_master.bat
./scripts/start_spark_worker.bat
```

5. **Lancer les producteurs**
```bash
python kafka_producers.py
```

6. **Lancer le consumer Spark**
```bash
python spark_streaming_consumer.py
```

7. **Ouvrir le dashboard**
```bash
streamlit run dashboard_3d_realtime.py
```

## 📊 Dashboard Features

- **Visualizations 3D** des trending keywords
- **Surface plots** pour évolution sentiment
- **Détection d'anomalies** en temps réel
- **Analytics cross-platform** sans redémarrage
- **Monitoring multi-sources** (Reddit, Twitter, IoT, News)

## 🔧 Configuration

### Kafka Topics
- `reddit_stream`: Données Reddit (3 partitions)
- `twitter_stream`: Données Twitter (3 partitions)  
- `iot_sensors`: Capteurs IoT (5 partitions)
- `news_feed`: Flux d'actualités (2 partitions)

### Services URLs
- Kafka: `localhost:9092`
- Spark UI: `http://localhost:8080`
- MongoDB: `mongodb://localhost:27017`
- Dashboard: `http://localhost:8501`

## 📈 Analytics Capabilities

- **Sentiment Analysis**: VADER + TextBlob + Lexicon-based
- **Keyword Trending**: Fenêtres glissantes avec scoring
- **Anomaly Detection**: Z-score et seuils statistiques
- **Cross-Source Correlation**: Analyse inter-plateformes
- **Real-Time Visualization**: Mises à jour sans interruption

## 🎯 Final Project Compliance

✅ **Multi-Source Data Ingestion**: Reddit, Twitter, IoT, News  
✅ **Apache Kafka**: Message streaming  
✅ **Spark Streaming**: Real-time processing  
✅ **Text Analytics**: NLP et sentiment analysis  
✅ **NoSQL Storage**: MongoDB intégration  
✅ **3D Visualizations**: Plotly 3D plots  
✅ **Real-Time Monitoring**: Dashboard temps réel  

## 🔧 Troubleshooting

### Java non trouvé
```bash
# Installer Java 8 ou 11
# Configurer JAVA_HOME
```

### Erreurs Kafka
```bash
# Vérifier Zookeeper actif
# Ports 9092, 2181 libres
```

### Erreurs Spark
```bash
# Vérifier SPARK_HOME
# Python et PySpark compatibles
```
