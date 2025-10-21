#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST COMPLET DU SYSTÈME MULTI-SOURCE ANALYTICS
Ce script vérifie tous les composants du système
"""

import json
import time
import requests
from kafka import KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from collections import defaultdict
from datetime import datetime

class SystemTester:
    """Testeur complet du système"""
    
    def __init__(self):
        self.results = {
            'kafka': {'status': '❌', 'details': []},
            'topics': {'status': '❌', 'details': []},
            'producers': {'status': '❌', 'details': []},
            'consumer': {'status': '❌', 'details': []},
            'dashboard': {'status': '❌', 'details': []}
        }
        
    def test_kafka_connection(self):
        """Test 1: Connexion à Kafka"""
        print("\n🔍 TEST 1: Connexion Kafka")
        print("-" * 50)
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=['localhost:9092'],
                request_timeout_ms=5000
            )
            topics = admin.list_topics()
            self.results['kafka']['status'] = '✅'
            self.results['kafka']['details'].append(f"Connecté à Kafka")
            self.results['kafka']['details'].append(f"{len(topics)} topics trouvés")
            print(f"✅ Kafka est en ligne")
            print(f"   {len(topics)} topics disponibles")
            admin.close()
            return True
        except Exception as e:
            self.results['kafka']['status'] = '❌'
            self.results['kafka']['details'].append(f"Erreur: {str(e)}")
            print(f"❌ Impossible de se connecter à Kafka: {e}")
            return False
    
    def test_required_topics(self):
        """Test 2: Vérification des topics requis"""
        print("\n🔍 TEST 2: Topics requis")
        print("-" * 50)
        required_topics = {
            'reddit_stream': 3,
            'twitter_stream': 3,
            'iot_sensors': 5,
            'news_feed': 2
        }
        
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=['localhost:9092'],
                request_timeout_ms=5000
            )
            existing_topics = admin.list_topics()
            
            all_present = True
            for topic_name, expected_partitions in required_topics.items():
                if topic_name in existing_topics:
                    metadata = admin.describe_topics([topic_name])
                    # kafka-python may return a dict or an object; handle both
                    partitions_info = None
                    if metadata and len(metadata) > 0:
                        topic_meta = metadata[0]
                        if isinstance(topic_meta, dict):
                            partitions_info = topic_meta.get('partitions')
                        else:
                            partitions_info = getattr(topic_meta, 'partitions', None)
                    if partitions_info is None:
                        partitions = 0
                    else:
                        partitions = len(partitions_info)
                    if partitions == expected_partitions:
                        print(f"✅ {topic_name}: {partitions} partitions")
                        self.results['topics']['details'].append(f"{topic_name}: OK ({partitions}p)")
                    else:
                        print(f"⚠️  {topic_name}: {partitions} partitions (attendu: {expected_partitions})")
                        self.results['topics']['details'].append(f"{topic_name}: Mauvais nb partitions")
                        all_present = False
                else:
                    print(f"❌ {topic_name}: MANQUANT")
                    self.results['topics']['details'].append(f"{topic_name}: MANQUANT")
                    all_present = False
            
            self.results['topics']['status'] = '✅' if all_present else '⚠️'
            admin.close()
            return all_present
        except Exception as e:
            self.results['topics']['status'] = '❌'
            self.results['topics']['details'].append(f"Erreur: {str(e)}")
            print(f"❌ Erreur lors de la vérification: {e}")
            return False
    
    def test_producers_activity(self, duration=30):
        """Test 3: Activité des producers"""
        print(f"\n🔍 TEST 3: Activité des Producers ({duration}s)")
        print("-" * 50)
        
        topics = ['reddit_stream', 'twitter_stream', 'iot_sensors', 'news_feed']
        message_counts = defaultdict(int)
        
        try:
            consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='latest',
                enable_auto_commit=False,
                consumer_timeout_ms=duration * 1000,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            
            print(f"📊 Écoute des messages pendant {duration} secondes...")
            start_time = time.time()
            # Use poll loop to avoid blocking iteration and allow timeout-based exit
            while time.time() - start_time < duration:
                remaining_ms = int((duration - (time.time() - start_time)) * 1000)
                # poll with a short timeout to collect messages
                records = consumer.poll(timeout_ms=min(1000, max(100, remaining_ms)))
                if not records:
                    # no new records in this poll
                    continue
                for tp, recs in records.items():
                    for rec in recs:
                        message_counts[rec.topic] += 1
                print(f"\r   Messages reçus: {sum(message_counts.values())} ", end='', flush=True)
                
            print()  # Nouvelle ligne après la barre
            
            consumer.close()
            
            # Vérification
            all_active = True
            for topic in topics:
                count = message_counts[topic]
                if count > 0:
                    print(f"✅ {topic}: {count} messages")
                    self.results['producers']['details'].append(f"{topic}: {count} msgs")
                else:
                    print(f"❌ {topic}: Aucun message")
                    self.results['producers']['details'].append(f"{topic}: Inactif")
                    all_active = False
            
            self.results['producers']['status'] = '✅' if all_active else '⚠️'
            return all_active
            
        except Exception as e:
            self.results['producers']['status'] = '❌'
            self.results['producers']['details'].append(f"Erreur: {str(e)}")
            print(f"❌ Erreur lors du test: {e}")
            return False
    
    def test_message_content(self, sample_size=10):
        """Test 4: Validation du contenu des messages"""
        print(f"\n🔍 TEST 4: Validation du contenu ({sample_size} échantillons)")
        print("-" * 50)
        
        topics = ['reddit_stream', 'twitter_stream', 'iot_sensors', 'news_feed']
        required_fields = {
            'reddit_stream': ['id', 'title', 'author', 'timestamp'],
            'twitter_stream': ['id', 'text', 'author', 'timestamp'],
            'iot_sensors': ['sensor_id', 'sensor_type', 'timestamp', 'metrics'],
            'news_feed': ['id', 'title', 'source', 'timestamp']
        }
        
        try:
            consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='latest',
                enable_auto_commit=False,
                consumer_timeout_ms=15000,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            
            samples = defaultdict(list)
            
            start_time = time.time()
            timeout_seconds = 15
            while time.time() - start_time < timeout_seconds:
                records = consumer.poll(timeout_ms=1000)
                if not records:
                    continue
                for tp, recs in records.items():
                    for rec in recs:
                        if len(samples[rec.topic]) < sample_size:
                            samples[rec.topic].append(rec.value)
                if all(len(s) >= sample_size for s in samples.values()):
                    break
            
            consumer.close()
            
            # Validation
            all_valid = True
            for topic, messages in samples.items():
                if len(messages) == 0:
                    print(f"⚠️  {topic}: Aucun échantillon")
                    self.results['consumer']['details'].append(f"{topic}: Pas de données")
                    continue
                
                valid_count = 0
                for msg in messages:
                    has_all_fields = all(field in msg for field in required_fields[topic])
                    if has_all_fields:
                        valid_count += 1
                
                if valid_count == len(messages):
                    print(f"✅ {topic}: {valid_count}/{len(messages)} messages valides")
                    self.results['consumer']['details'].append(f"{topic}: Structure OK")
                else:
                    print(f"⚠️  {topic}: {valid_count}/{len(messages)} messages valides")
                    self.results['consumer']['details'].append(f"{topic}: Structure incorrecte")
                    all_valid = False
            
            self.results['consumer']['status'] = '✅' if all_valid else '⚠️'
            return all_valid
            
        except Exception as e:
            self.results['consumer']['status'] = '❌'
            self.results['consumer']['details'].append(f"Erreur: {str(e)}")
            print(f"❌ Erreur lors de la validation: {e}")
            return False
    
    def test_dashboard(self):
        """Test 5: Dashboard Streamlit"""
        print("\n🔍 TEST 5: Dashboard Streamlit")
        print("-" * 50)
        
        try:
            response = requests.get('http://localhost:8505', timeout=5)
            if response.status_code == 200:
                print(f"✅ Dashboard accessible sur http://localhost:8505")
                self.results['dashboard']['status'] = '✅'
                self.results['dashboard']['details'].append("Dashboard en ligne")
                return True
            else:
                print(f"⚠️  Dashboard répond avec status {response.status_code}")
                self.results['dashboard']['status'] = '⚠️'
                self.results['dashboard']['details'].append(f"Status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"❌ Dashboard non accessible sur http://localhost:8505")
            self.results['dashboard']['status'] = '❌'
            self.results['dashboard']['details'].append("Connexion refusée")
            return False
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            self.results['dashboard']['status'] = '❌'
            self.results['dashboard']['details'].append(f"Erreur: {str(e)}")
            return False
    
    def print_summary(self):
        """Affiche le résumé des tests"""
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        components = [
            ('Kafka Broker', self.results['kafka']),
            ('Topics Configuration', self.results['topics']),
            ('Producers Activity', self.results['producers']),
            ('Message Validation', self.results['consumer']),
            ('Dashboard', self.results['dashboard'])
        ]
        
        for name, result in components:
            status = result['status']
            print(f"\n{status} {name}")
            for detail in result['details']:
                print(f"   • {detail}")
        
        # Score global
        statuses = [r['status'] for _, r in components]
        success_count = sum(1 for s in statuses if s == '✅')
        warning_count = sum(1 for s in statuses if s == '⚠️')
        failure_count = sum(1 for s in statuses if s == '❌')
        
        print("\n" + "=" * 60)
        print(f"🎯 SCORE GLOBAL: {success_count}/{len(components)} composants OK")
        if warning_count > 0:
            print(f"⚠️  {warning_count} avertissement(s)")
        if failure_count > 0:
            print(f"❌ {failure_count} échec(s)")
        print("=" * 60)
        
        return failure_count == 0

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🧪 TEST COMPLET DU SYSTÈME MULTI-SOURCE ANALYTICS")
    print("=" * 60)
    print(f"⏰ Début des tests: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = SystemTester()
    
    # Exécution des tests
    tests = [
        ("Kafka Connection", tester.test_kafka_connection),
        ("Required Topics", tester.test_required_topics),
        ("Producers Activity", lambda: tester.test_producers_activity(duration=20)),
        ("Message Content", lambda: tester.test_message_content(sample_size=5)),
        ("Dashboard", tester.test_dashboard)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    tester.print_summary()
    
    print(f"\n⏰ Fin des tests: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Code de sortie
    all_passed = tester.print_summary()
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
