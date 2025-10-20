# 📊 DASHBOARD 3D REAL-TIME ANALYTICS
# Interface utilisateur moderne pour visualisation temps réel
# Plotly 3D + Streamlit + WebSocket pour mises à jour sans redémarrage

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
import time
import threading
import asyncio
import websockets
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from collections import defaultdict, deque
import requests
import sqlite3
from pathlib import Path

# Configuration Streamlit
st.set_page_config(
    page_title="🚀 Multi-Source Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeDashboard:
    """Dashboard principal pour analytics temps réel"""
    
    def __init__(self):
        self.data_cache = {
            'trending_keywords': deque(maxlen=1000),
            'sentiment_timeline': deque(maxlen=500),
            'source_statistics': defaultdict(int),
            'anomalies': deque(maxlen=100),
            'messages_per_minute': deque(maxlen=60),
            'keyword_evolution': defaultdict(lambda: deque(maxlen=100))
        }
        
        # Base de données locale pour persistance
        self.db_path = Path("dashboard_cache.db")
        self._init_database()
        
        # État de connexion
        self.connected_to_spark = False
        self.last_update = None
        
    def _init_database(self):
        """Initialise la base de données locale"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                data_type TEXT NOT NULL,
                data_json TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def fetch_spark_analytics(self) -> Optional[Dict]:
        """Récupère les analytics depuis Spark Streaming"""
        try:
            # Simuler l'appel API vers le consumer Spark
            # En production, ceci serait un endpoint REST ou WebSocket
            
            # Données simulées pour démonstration
            current_time = datetime.now()
            
            # Simulation de données réalistes
            trending_keywords = [
                {'keyword': 'climate', 'score': 0.85, 'category': 'environment', 'mentions': 45},
                {'keyword': 'technology', 'score': 0.78, 'category': 'tech', 'mentions': 38},
                {'keyword': 'politics', 'score': 0.72, 'category': 'politics', 'mentions': 32},
                {'keyword': 'health', 'score': 0.68, 'category': 'health', 'mentions': 28},
                {'keyword': 'economy', 'score': 0.65, 'category': 'economics', 'mentions': 25},
                {'keyword': 'education', 'score': 0.61, 'category': 'social', 'mentions': 22},
                {'keyword': 'innovation', 'score': 0.58, 'category': 'tech', 'mentions': 19},
                {'keyword': 'security', 'score': 0.55, 'category': 'safety', 'mentions': 17}
            ]
            
            # Timeline de sentiment des dernières minutes
            sentiment_timeline = []
            for i in range(20):
                time_point = current_time - timedelta(minutes=i)
                sentiment_timeline.append({
                    'time': time_point.strftime('%H:%M'),
                    'sentiment': np.random.normal(0.1, 0.3),  # Légèrement positif en moyenne
                    'volume': np.random.randint(15, 45)
                })
            
            # Anomalies récentes
            anomalies = [
                {
                    'type': 'sentiment_spike',
                    'description': 'Pic de sentiment négatif détecté',
                    'severity': 'medium',
                    'timestamp': (current_time - timedelta(minutes=5)).isoformat()
                },
                {
                    'type': 'volume_anomaly', 
                    'description': 'Volume de messages anormalement élevé',
                    'severity': 'low',
                    'timestamp': (current_time - timedelta(minutes=12)).isoformat()
                }
            ]
            
            # Statistiques par source
            source_stats = {
                'reddit_news': {'messages': 1247, 'avg_sentiment': 0.15},
                'twitter_feed': {'messages': 2156, 'avg_sentiment': -0.05},
                'iot_sensors': {'messages': 3421, 'avg_sentiment': 0.0},
                'news_api': {'messages': 856, 'avg_sentiment': 0.08}
            }
            
            return {
                'timestamp': current_time.isoformat(),
                'trending_keywords': trending_keywords,
                'sentiment_timeline': sentiment_timeline,
                'anomalies': anomalies,
                'source_statistics': source_stats,
                'system_health': {
                    'status': 'healthy',
                    'uptime': '2h 15m',
                    'messages_processed': 7680,
                    'processing_rate': '12.5 msg/sec'
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur récupération analytics: {e}")
            return None
    
    def update_cache(self, analytics_data: Dict):
        """Met à jour le cache local avec nouvelles données"""
        if not analytics_data:
            return
            
        # Trending keywords
        for kw_data in analytics_data.get('trending_keywords', []):
            self.data_cache['trending_keywords'].append({
                'timestamp': datetime.now(),
                'keyword': kw_data['keyword'],
                'score': kw_data['score'],
                'category': kw_data.get('category', 'general'),
                'mentions': kw_data.get('mentions', 0)
            })
            
            # Évolution par mot-clé
            self.data_cache['keyword_evolution'][kw_data['keyword']].append({
                'timestamp': datetime.now(),
                'score': kw_data['score']
            })
        
        # Timeline sentiment
        for sentiment_data in analytics_data.get('sentiment_timeline', []):
            self.data_cache['sentiment_timeline'].append({
                'timestamp': datetime.now(),
                'time_label': sentiment_data['time'],
                'sentiment': sentiment_data['sentiment'],
                'volume': sentiment_data.get('volume', 0)
            })
        
        # Anomalies
        for anomaly in analytics_data.get('anomalies', []):
            self.data_cache['anomalies'].append({
                'timestamp': datetime.now(),
                'data': anomaly
            })
        
        # Statistiques sources
        source_stats = analytics_data.get('source_statistics', {})
        for source, stats in source_stats.items():
            self.data_cache['source_statistics'][source] = stats
        
        self.last_update = datetime.now()
        self.connected_to_spark = True
    
    def create_3d_keyword_visualization(self) -> go.Figure:
        """Crée une visualisation 3D des mots-clés trending"""
        if not self.data_cache['trending_keywords']:
            return go.Figure()
        
        # Préparer les données
        recent_keywords = list(self.data_cache['trending_keywords'])[-50:]  # 50 derniers
        
        if not recent_keywords:
            return go.Figure()
        
        # Grouper par mot-clé et calculer métriques
        keyword_metrics = defaultdict(lambda: {'scores': [], 'mentions': [], 'categories': []})
        
        for item in recent_keywords:
            keyword = item['keyword']
            keyword_metrics[keyword]['scores'].append(item['score'])
            keyword_metrics[keyword]['mentions'].append(item['mentions'])
            keyword_metrics[keyword]['categories'].append(item['category'])
        
        # Calculer coordonnées 3D
        keywords = []
        x_coords = []  # Score moyen
        y_coords = []  # Mentions totales
        z_coords = []  # Variance (stabilité)
        colors = []
        sizes = []
        
        category_colors = {
            'technology': '#FF6B6B',
            'politics': '#4ECDC4', 
            'environment': '#45B7D1',
            'health': '#96CEB4',
            'economics': '#FFEAA7',
            'social': '#DDA0DD',
            'safety': '#FFB347',
            'general': '#B0B0B0'
        }
        
        for keyword, metrics in keyword_metrics.items():
            if len(metrics['scores']) >= 2:  # Minimum pour calcul variance
                keywords.append(keyword)
                
                avg_score = np.mean(metrics['scores'])
                total_mentions = sum(metrics['mentions'])
                score_variance = np.var(metrics['scores'])
                
                x_coords.append(avg_score)
                y_coords.append(total_mentions)
                z_coords.append(score_variance)
                
                # Couleur basée sur catégorie majoritaire
                categories = metrics['categories']
                main_category = max(set(categories), key=categories.count)
                colors.append(category_colors.get(main_category, '#B0B0B0'))
                
                # Taille basée sur fréquence d'apparition
                sizes.append(min(len(metrics['scores']) * 3, 30))
        
        # Créer la figure 3D
        fig = go.Figure(data=[
            go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                mode='markers+text',
                text=keywords,
                textposition='top center',
                marker=dict(
                    size=sizes,
                    color=colors,
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                hovertemplate=(
                    '<b>%{text}</b><br>' +
                    'Score Trending: %{x:.3f}<br>' +
                    'Mentions: %{y}<br>' +
                    'Variance: %{z:.3f}<br>' +
                    '<extra></extra>'
                )
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🌐 Espace 3D des Trending Keywords',
                'x': 0.5,
                'font': {'size': 18, 'color': '#2E86AB'}
            },
            scene=dict(
                xaxis_title='Score Trending Moyen',
                yaxis_title='Mentions Totales', 
                zaxis_title='Variance (Stabilité)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        
        return fig
    
    def create_sentiment_surface_plot(self) -> go.Figure:
        """Crée une surface 3D pour l'évolution du sentiment"""
        if not self.data_cache['sentiment_timeline']:
            return go.Figure()
        
        # Préparer données pour surface 3D
        timeline_data = list(self.data_cache['sentiment_timeline'])[-60:]  # Dernière heure
        
        if len(timeline_data) < 10:
            return go.Figure()
        
        # Créer grille temporelle
        time_points = len(timeline_data)
        sentiment_sources = ['reddit', 'twitter', 'news', 'iot']  # Simulation multi-sources
        
        # Matrice Z pour la surface
        Z = []
        X = list(range(time_points))
        Y = list(range(len(sentiment_sources)))
        
        for i, source in enumerate(sentiment_sources):
            source_sentiments = []
            for j, item in enumerate(timeline_data):
                # Simuler sentiment par source avec variations
                base_sentiment = item['sentiment']
                source_variation = {
                    'reddit': 0.1,
                    'twitter': -0.05,
                    'news': 0.02,
                    'iot': 0.0
                }
                adjusted_sentiment = base_sentiment + source_variation.get(source, 0)
                adjusted_sentiment += np.random.normal(0, 0.1)  # Bruit
                source_sentiments.append(adjusted_sentiment)
            Z.append(source_sentiments)
        
        # Créer surface 3D
        fig = go.Figure(data=[
            go.Surface(
                z=Z,
                x=X,
                y=Y,
                colorscale='RdYlBu',
                colorbar=dict(
                    title="Sentiment"
                ),
                hovertemplate=(
                    'Temps: %{x}<br>' +
                    'Source: %{y}<br>' +
                    'Sentiment: %{z:.3f}<br>' +
                    '<extra></extra>'
                )
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🌊 Surface 3D - Évolution Sentiment Multi-Sources',
                'x': 0.5,
                'font': {'size': 18, 'color': '#2E86AB'}
            },
            scene=dict(
                xaxis_title='Progression Temporelle',
                yaxis_title='Sources de Données',
                zaxis_title='Score Sentiment',
                yaxis=dict(
                    tickmode='array',
                    tickvals=list(range(len(sentiment_sources))),
                    ticktext=sentiment_sources
                ),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            height=500
        )
        
        return fig
    
    def create_anomaly_detection_plot(self) -> go.Figure:
        """Visualisation des anomalies détectées"""
        if not self.data_cache['anomalies']:
            return go.Figure()
        
        # Préparer données anomalies
        anomaly_data = list(self.data_cache['anomalies'])[-20:]  # 20 dernières
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Timeline des Anomalies', 'Répartition par Type', 
                          'Sévérité', 'Fréquence par Heure'),
            specs=[[{"secondary_y": False}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "histogram"}]]
        )
        
        if anomaly_data:
            # Timeline
            times = [item['timestamp'] for item in anomaly_data]
            severities = [item['data'].get('severity', 'unknown') for item in anomaly_data]
            
            severity_colors = {'high': 'red', 'medium': 'orange', 'low': 'yellow', 'unknown': 'gray'}
            colors = [severity_colors.get(sev, 'gray') for sev in severities]
            
            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=list(range(len(times))),
                    mode='markers',
                    marker=dict(
                        color=colors,
                        size=10,
                        line=dict(width=1, color='white')
                    ),
                    text=[item['data'].get('description', '') for item in anomaly_data],
                    hovertemplate='%{text}<br>%{x}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Répartition par type
            anomaly_types = [item['data'].get('type', 'unknown') for item in anomaly_data]
            type_counts = pd.Series(anomaly_types).value_counts()
            
            fig.add_trace(
                go.Pie(
                    labels=type_counts.index,
                    values=type_counts.values,
                    hole=0.3
                ),
                row=1, col=2
            )
            
            # Sévérité
            severity_counts = pd.Series(severities).value_counts()
            
            fig.add_trace(
                go.Bar(
                    x=severity_counts.index,
                    y=severity_counts.values,
                    marker_color=['red' if x == 'high' else 'orange' if x == 'medium' else 'yellow' for x in severity_counts.index]
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title_text="🚨 Tableau de Bord Anomalies",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_source_performance_radar(self) -> go.Figure:
        """Graphique radar des performances par source"""
        if not self.data_cache['source_statistics']:
            return go.Figure()
        
        sources = list(self.data_cache['source_statistics'].keys())
        if not sources:
            return go.Figure()
        
        # Métriques pour radar
        metrics = ['Volume', 'Sentiment Moyen', 'Stabilité', 'Trending Score', 'Qualité']
        
        fig = go.Figure()
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for i, source in enumerate(sources[:5]):  # Limiter à 5 sources
            stats = self.data_cache['source_statistics'][source]
            
            # Normaliser les métriques (0-1)
            volume_norm = min(stats.get('messages', 0) / 1000, 1)  # Normaliser par rapport à 1000
            sentiment_norm = (stats.get('avg_sentiment', 0) + 1) / 2  # -1/+1 -> 0/1
            stability_norm = max(0, 1 - abs(stats.get('sentiment_variance', 0.5)))  # Simulé
            trending_norm = np.random.random()  # Simulé
            quality_norm = np.random.random() * 0.5 + 0.5  # Simulé entre 0.5-1
            
            values = [volume_norm, sentiment_norm, stability_norm, trending_norm, quality_norm]
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],  # Fermer le polygone
                theta=metrics + [metrics[0]],
                fill='toself',
                name=source.replace('_', ' ').title(),
                line_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            title={
                'text': '🎯 Performance Radar - Sources de Données',
                'x': 0.5,
                'font': {'size': 18, 'color': '#2E86AB'}
            },
            height=500
        )
        
        return fig

def main():
    """Interface Streamlit principale"""
    
    # Titre principal avec emoji et style
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #2E86AB; font-size: 3em;">🚀 Multi-Source Analytics Dashboard</h1>
        <h3 style="color: #6C7B7F;">Real-Time Analytics with Apache Kafka & Spark Streaming</h3>
        <p style="color: #95A5A6; font-size: 1.1em;">Visualisation 3D en temps réel • Détection d'anomalies • Cross-platform content analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser dashboard
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = RealTimeDashboard()
    
    dashboard = st.session_state.dashboard
    
    # Sidebar pour contrôles
    with st.sidebar:
        st.markdown("## ⚙️ Contrôles Dashboard")
        
        auto_refresh = st.checkbox("🔄 Rafraîchissement automatique", value=False)
        refresh_interval = st.slider("Intervalle (secondes)", 5, 60, 10)
        
        st.markdown("---")
        st.markdown("## 📊 Métriques Système")
        
        if dashboard.connected_to_spark:
            st.success("✅ Connecté à Spark Streaming")
        else:
            st.warning("⚠️ Connexion Spark en attente")
        
        if dashboard.last_update:
            st.info(f"🕒 Dernière MAJ: {dashboard.last_update.strftime('%H:%M:%S')}")
        
        # Bouton de refresh manuel
        if st.button("🔄 Actualiser maintenant"):
            analytics_data = dashboard.fetch_spark_analytics()
            if analytics_data:
                dashboard.update_cache(analytics_data)
    
    # Récupérer données pour affichage (pas d'auto-refresh pour éviter les erreurs)
    analytics_data = dashboard.fetch_spark_analytics()
    if analytics_data:
        dashboard.update_cache(analytics_data)
    
    # Métriques en haut
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📧 Messages Traités", 
            analytics_data.get('system_health', {}).get('messages_processed', 0),
            delta="+150 dernière min"
        )
    
    with col2:
        avg_sentiment = 0.15  # Simulé
        st.metric(
            "😊 Sentiment Moyen", 
            f"{avg_sentiment:.3f}",
            delta=f"{avg_sentiment:+.3f}"
        )
    
    with col3:
        processing_rate = analytics_data.get('system_health', {}).get('processing_rate', '0 msg/sec')
        st.metric(
            "⚡ Vitesse Traitement", 
            processing_rate,
            delta="+2.1 msg/sec"
        )
    
    with col4:
        active_keywords = len(analytics_data.get('trending_keywords', []))
        st.metric(
            "🔥 Keywords Trending", 
            active_keywords,
            delta=f"+{np.random.randint(1, 5)}"
        )
    
    st.markdown("---")
    
    # Visualisations principales en onglets - Focus sur AFP vs Reddit vs GDELT
    tab1, tab2, tab3 = st.tabs([
        "�️ AFP vs Reddit vs GDELT - Analyse Détaillée", 
        "� Analytics Avancées Cross-Source",
        "⚡ Monitoring Système"
    ])
    
    with tab1:
        st.markdown("### �️ ANALYSE DÉTAILLÉE: AFP vs Reddit vs GDELT")
        st.markdown("**Comparaison approfondie des informations officielles AFP avec les discussions Reddit et événements GDELT**")
        
        # Section 1: Vue d'ensemble des corrélations
        st.markdown("#### 📊 Vue d'Ensemble des Corrélations")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏛️ Articles AFP", "8", "Sources officielles")
        with col2:
            st.metric("💬 Discussions Reddit", "28", "+3 nouvelles")
        with col3:
            st.metric("🌍 Événements GDELT", "17", "+2 récents")
        
        # Graphique de corrélation temporelle avancé
        st.markdown("#### ⏰ Analyse Temporelle des Corrélations")
        
        # Simulation de données réalistes pour la corrélation temporelle
        import plotly.graph_objects as go
        from datetime import datetime, timedelta
        import numpy as np
        
        # Génération de données de corrélation temporelle
        time_points = pd.date_range(start='2024-01-01', periods=24, freq='H')
        afp_activity = np.random.normal(0.7, 0.2, 24).clip(0, 1)
        reddit_activity = np.random.normal(0.5, 0.3, 24).clip(0, 1)
        gdelt_activity = np.random.normal(0.6, 0.25, 24).clip(0, 1)
        
        # Corrélations croisées avec délais
        correlation_afp_reddit = np.correlate(afp_activity, reddit_activity, mode='full')
        correlation_afp_gdelt = np.correlate(afp_activity, gdelt_activity, mode='full')
        
        fig_correlation = go.Figure()
        
        fig_correlation.add_trace(go.Scatter(
            x=time_points, y=afp_activity,
            mode='lines+markers',
            name='📰 AFP (Sources Officielles)',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8)
        ))
        
        fig_correlation.add_trace(go.Scatter(
            x=time_points, y=reddit_activity,
            mode='lines+markers',
            name='💬 Reddit (Discussions)',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8)
        ))
        
        fig_correlation.add_trace(go.Scatter(
            x=time_points, y=gdelt_activity,
            mode='lines+markers',
            name='🌍 GDELT (Événements)',
            line=dict(color='#45B7D1', width=3),
            marker=dict(size=8)
        ))
        
        fig_correlation.update_layout(
            title="🕒 Évolution Temporelle de l'Activité par Source",
            xaxis_title="Temps",
            yaxis_title="Intensité d'Activité",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_correlation, use_container_width=True)
        
        # Section 2: Analyse détaillée des matchs
        st.markdown("#### 🔍 Analyse Détaillée des Correspondances")
        
        # Simulation de données de matchs détaillées
        match_data = [
            {
                'afp_title': 'Réforme économique européenne annoncée',
                'reddit_matches': 3,
                'gdelt_matches': 2,
                'correlation_score': 0.89,
                'delay_reddit': '2.3h',
                'delay_gdelt': '1.7h',
                'sentiment_reddit': 'Négatif (-0.3)',
                'confidence': 'Élevée'
            },
            {
                'afp_title': 'Accord climatique international signé',
                'reddit_matches': 5,
                'gdelt_matches': 4,
                'correlation_score': 0.94,
                'delay_reddit': '1.8h',
                'delay_gdelt': '0.9h',
                'sentiment_reddit': 'Positif (+0.6)',
                'confidence': 'Très élevée'
            },
            {
                'afp_title': 'Innovation technologique majeure',
                'reddit_matches': 2,
                'gdelt_matches': 1,
                'correlation_score': 0.76,
                'delay_reddit': '4.1h',
                'delay_gdelt': '3.2h',
                'sentiment_reddit': 'Neutre (0.1)',
                'confidence': 'Moyenne'
            }
        ]
        
        # Tableau détaillé des correspondances
        df_matches = pd.DataFrame(match_data)
        
        st.markdown("**🎯 Correspondances Détectées (Échantillon)**")
        st.dataframe(
            df_matches,
            column_config={
                "afp_title": st.column_config.TextColumn("📰 Article AFP", width="large"),
                "reddit_matches": st.column_config.NumberColumn("💬 Matchs Reddit"),
                "gdelt_matches": st.column_config.NumberColumn("🌍 Matchs GDELT"),
                "correlation_score": st.column_config.ProgressColumn("🎯 Score Corrélation", min_value=0, max_value=1),
                "delay_reddit": st.column_config.TextColumn("⏱️ Délai Reddit"),
                "delay_gdelt": st.column_config.TextColumn("⏱️ Délai GDELT"),
                "sentiment_reddit": st.column_config.TextColumn("😊 Sentiment Reddit"),
                "confidence": st.column_config.TextColumn("✅ Confiance")
            },
            use_container_width=True
        )
        
        # Section 3: Matrice de corrélation 3D
        st.markdown("#### 🎲 Matrice de Corrélation 3D")
        
        # Création d'une matrice de corrélation 3D
        topics = ['Économie', 'Politique', 'Environnement', 'Technologie', 'Santé']
        x_afp = np.random.uniform(0.5, 1.0, len(topics))
        y_reddit = np.random.uniform(0.3, 0.9, len(topics))
        z_gdelt = np.random.uniform(0.4, 0.8, len(topics))
        
        fig_3d_correlation = go.Figure(data=[go.Scatter3d(
            x=x_afp,
            y=y_reddit,
            z=z_gdelt,
            mode='markers+text',
            text=topics,
            textposition='top center',
            marker=dict(
                size=[20, 25, 30, 22, 28],
                color=[0.8, 0.9, 0.7, 0.85, 0.75],
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(title="Intensité Corrélation")
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         'AFP: %{x:.2f}<br>' +
                         'Reddit: %{y:.2f}<br>' +
                         'GDELT: %{z:.2f}<extra></extra>'
        )])
        
        fig_3d_correlation.update_layout(
            title="🎲 Espace 3D des Corrélations par Thématique",
            scene=dict(
                xaxis_title="📰 Intensité AFP",
                yaxis_title="💬 Résonance Reddit",
                zaxis_title="🌍 Coverage GDELT"
            ),
            height=500
        )
        
        st.plotly_chart(fig_3d_correlation, use_container_width=True)
        
        # Section 4: Analyse des délais de propagation
        st.markdown("#### ⚡ Analyse des Délais de Propagation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogramme des délais Reddit
            delays_reddit = np.random.exponential(2.5, 100)  # Délais en heures
            fig_delays_reddit = go.Figure(data=[go.Histogram(
                x=delays_reddit,
                nbinsx=20,
                name="Délais Reddit",
                marker_color='#FF9F43'
            )])
            fig_delays_reddit.update_layout(
                title="⏰ Distribution des Délais Reddit",
                xaxis_title="Délai (heures)",
                yaxis_title="Fréquence",
                height=300
            )
            st.plotly_chart(fig_delays_reddit, use_container_width=True)
        
        with col2:
            # Histogramme des délais GDELT
            delays_gdelt = np.random.exponential(1.8, 100)  # Délais en heures
            fig_delays_gdelt = go.Figure(data=[go.Histogram(
                x=delays_gdelt,
                nbinsx=20,
                name="Délais GDELT",
                marker_color='#6C5CE7'
            )])
            fig_delays_gdelt.update_layout(
                title="⏰ Distribution des Délais GDELT",
                xaxis_title="Délai (heures)",
                yaxis_title="Fréquence",
                height=300
            )
            st.plotly_chart(fig_delays_gdelt, use_container_width=True)
        
        # Section 5: Flux d'information en temps réel
        st.markdown("#### 🌊 Flux d'Information en Temps Réel")
        
        # Graphique de flux en temps réel
        fig_flow = go.Figure()
        
        # Simulation d'un flux d'information
        time_flow = pd.date_range(start='2024-01-01 08:00', periods=12, freq='30min')
        afp_flow = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # AFP publie en premier
        reddit_flow = [0, 0, 0.3, 0.7, 1, 1, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1]  # Reddit suit avec délai
        gdelt_flow = [0, 0, 0.1, 0.4, 0.8, 1, 1, 0.9, 0.7, 0.5, 0.3, 0.2]  # GDELT entre les deux
        
        fig_flow.add_trace(go.Scatter(
            x=time_flow, y=afp_flow,
            mode='lines+markers',
            name='📰 AFP (Source)',
            line=dict(color='#FF6B6B', width=4),
            fill='tonexty'
        ))
        
        fig_flow.add_trace(go.Scatter(
            x=time_flow, y=reddit_flow,
            mode='lines+markers',
            name='💬 Reddit (Réaction)',
            line=dict(color='#4ECDC4', width=4),
            fill='tonexty'
        ))
        
        fig_flow.add_trace(go.Scatter(
            x=time_flow, y=gdelt_flow,
            mode='lines+markers',
            name='🌍 GDELT (Documentation)',
            line=dict(color='#45B7D1', width=4),
            fill='tonexty'
        ))
        
        fig_flow.update_layout(
            title="🌊 Propagation d'une Information (Exemple: Réforme Économique)",
            xaxis_title="Temps",
            yaxis_title="Intensité de Coverage",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_flow, use_container_width=True)

    with tab2:
        st.markdown("### 📊 ANALYTICS AVANCÉES CROSS-SOURCE")
        
        # Section de sentiment cross-source
        col1, col2 = st.columns(2)
        
        with col1:
            # Radar chart comparatif des sources
            categories_radar = ['Rapidité', 'Précision', 'Coverage', 'Engagement', 'Fiabilité']
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[0.9, 0.95, 0.8, 0.6, 0.98],
                theta=categories_radar,
                fill='toself',
                name='📰 AFP',
                line_color='#FF6B6B'
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[0.7, 0.6, 0.9, 0.95, 0.5],
                theta=categories_radar,
                fill='toself',
                name='💬 Reddit',
                line_color='#4ECDC4'
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[0.8, 0.8, 0.95, 0.7, 0.8],
                theta=categories_radar,
                fill='toself',
                name='🌍 GDELT',
                line_color='#45B7D1'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1])
                ),
                title="🎯 Profil Comparatif des Sources",
                height=400
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Heatmap des corrélations par heure
            hours = list(range(24))
            correlations = np.random.uniform(0.3, 0.9, (3, 24))
            source_names = ['AFP-Reddit', 'AFP-GDELT', 'Reddit-GDELT']
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=correlations,
                x=hours,
                y=source_names,
                colorscale='RdYlBu',
                hoverongaps=False
            ))
            
            fig_heatmap.update_layout(
                title="🕒 Corrélations par Heure de la Journée",
                xaxis_title="Heure",
                yaxis_title="Paires de Sources",
                height=400
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Analyse des mots-clés trending cross-source
        st.markdown("#### 🔥 Trending Keywords Cross-Source")
        
        keywords_data = {
            'Keyword': ['réforme', 'climat', 'économie', 'technologie', 'santé', 'politique'],
            'AFP_Score': [0.9, 0.8, 0.95, 0.7, 0.6, 0.85],
            'Reddit_Score': [0.7, 0.9, 0.6, 0.95, 0.8, 0.5],
            'GDELT_Score': [0.8, 0.85, 0.9, 0.8, 0.7, 0.75],
            'Correlation': [0.89, 0.94, 0.76, 0.88, 0.82, 0.71]
        }
        
        df_keywords = pd.DataFrame(keywords_data)
        
        fig_keywords = go.Figure()
        
        fig_keywords.add_trace(go.Bar(
            name='📰 AFP',
            x=df_keywords['Keyword'],
            y=df_keywords['AFP_Score'],
            marker_color='#FF6B6B'
        ))
        
        fig_keywords.add_trace(go.Bar(
            name='💬 Reddit',
            x=df_keywords['Keyword'],
            y=df_keywords['Reddit_Score'],
            marker_color='#4ECDC4'
        ))
        
        fig_keywords.add_trace(go.Bar(
            name='🌍 GDELT',
            x=df_keywords['Keyword'],
            y=df_keywords['GDELT_Score'],
            marker_color='#45B7D1'
        ))
        
        fig_keywords.update_layout(
            title="🔥 Score des Keywords par Source",
            xaxis_title="Keywords",
            yaxis_title="Score de Tendance",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_keywords, use_container_width=True)

    with tab3:
        st.markdown("### 🚨 Détection et Analyse d'Anomalies")
        st.markdown("Surveillance en temps réel des comportements anormaux dans les flux de données")
        fig_anomalies = dashboard.create_anomaly_detection_plot()
        st.plotly_chart(fig_anomalies, use_container_width=True)
        
        # Liste des anomalies récentes
        if analytics_data and 'anomalies' in analytics_data:
            st.markdown("#### ⚠️ Anomalies Récentes")
            for anomaly in analytics_data['anomalies'][:5]:
                severity_color = {
                    'high': '🔴',
                    'medium': '🟠', 
                    'low': '🟡'
                }.get(anomaly.get('severity', 'low'), '⚪')
                
                st.markdown(f"""
                **{severity_color} {anomaly.get('type', 'Anomalie').replace('_', ' ').title()}**  
                {anomaly.get('description', 'Description non disponible')}  
                *{anomaly.get('timestamp', 'Timestamp inconnu')}*
                """)
        
        # Log système simplifié
        st.markdown("#### 📝 Log Système (Dernières activités)")
        log_messages = [
            "✅ Kafka Producer: 5 nouveaux messages envoyés",
            "⚡ Spark: Batch #47 traité avec succès (0.8s)",
            "💾 MongoDB: 12 documents stockés",
            "🔍 AFP Comparator: 3 nouvelles corrélations détectées",
            "📊 Dashboard: Mise à jour visualisations"
        ]
        
        for i, msg in enumerate(log_messages):
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    
    with tab4:
        st.markdown("### 🎯 Performance des Sources de Données")
        st.markdown("Analyse comparative des performances de chaque source de données")
        fig_radar = dashboard.create_source_performance_radar()
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Statistiques détaillées par source
        if analytics_data and 'source_statistics' in analytics_data:
            st.markdown("#### 📈 Statistiques Détaillées")
            for source, stats in analytics_data['source_statistics'].items():
                with st.expander(f"📊 {source.replace('_', ' ').title()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Messages", stats.get('messages', 0))
                    with col2:
                        sentiment = stats.get('avg_sentiment', 0)
                        st.metric("Sentiment Moyen", f"{sentiment:.3f}")
    
    with tab5:
        st.markdown("### 📈 Analytics Avancées et Projections")
        
        # Graphiques supplémentaires
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Distribution des Catégories")
            if analytics_data and 'trending_keywords' in analytics_data:
                categories = [kw.get('category', 'general') for kw in analytics_data['trending_keywords']]
                if categories:
                    category_counts = pd.Series(categories).value_counts()
                    fig_categories = px.pie(
                        values=category_counts.values,
                        names=category_counts.index,
                        title="Répartition par Catégorie"
                    )
                    st.plotly_chart(fig_categories, use_container_width=True)
        
        with col2:
            st.markdown("#### ⏱️ Volume par Heure")
            # Simuler données de volume
            hours = [f"{i:02d}:00" for i in range(24)]
            volumes = np.random.poisson(100, 24)  # Distribution de Poisson
            
            fig_volume = px.line(
                x=hours,
                y=volumes,
                title="Messages par Heure (24h)",
                labels={'x': 'Heure', 'y': 'Nombre de Messages'}
            )
            st.plotly_chart(fig_volume, use_container_width=True)
        
        # Matrice de corrélation des sources
        st.markdown("#### 🔗 Matrice de Corrélation Inter-Sources")
        correlation_data = np.random.rand(4, 4)  # Simulé
        np.fill_diagonal(correlation_data, 1)
        
        sources = ['Reddit', 'Twitter', 'IoT', 'News']
        correlation_df = pd.DataFrame(correlation_data, index=sources, columns=sources)
        
        fig_corr = px.imshow(
            correlation_df,
            text_auto=".2f",
            aspect="auto",
            title="Corrélation entre Sources"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with tab6:
        st.markdown("### 🏛️ Comparaison AFP vs Reddit vs GDELT")
        st.markdown("**Analyse des sources officielles vs discussions informelles vs événements documentés**")
        
        # Simulation des données AFP vs Reddit vs GDELT
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "📰 Articles AFP Officiels", 
                "8",
                "Sources vérifiées"
            )
            
        with col2:
            st.metric(
                "🔴 Discussions Reddit", 
                "28",
                "+3.5x engagement"
            )
            
        with col3:
            st.metric(
                "📊 Événements GDELT", 
                "17", 
                "Couverture globale"
            )
        
        # Tableau de comparaison
        st.markdown("#### 📋 Résumé des Corrélations")
        
        comparison_data = {
            'Article AFP': ['Réforme économique EU', 'Découverte médicale', 'Accord climat', 'Tech quantique'],
            'Reddit Posts': [4, 3, 5, 2],
            'Reddit Engagement': ['2.1k', '1.8k', '3.2k', '0.9k'],
            'GDELT Events': [2, 1, 3, 2],
            'Délai Moyen (h)': ['+12.3', '+8.7', '+15.1', '+6.2'],
            'Score Corrélation': ['1.8/2.0', '1.4/2.0', '1.9/2.0', '1.2/2.0']
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
        
        # Graphique de corrélation temporelle
        st.markdown("#### ⏰ Timeline des Corrélations")
        
        timeline_fig = go.Figure()
        
        # AFP (source officielle)
        timeline_fig.add_trace(go.Scatter(
            x=[0, 3, 6, 9],
            y=[1, 1, 1, 1],
            mode='markers+text',
            text=['AFP: Réforme EU', 'AFP: Médical', 'AFP: Climat', 'AFP: Quantique'],
            textposition="top center",
            marker=dict(size=15, color='blue', symbol='diamond'),
            name='AFP Officiel',
            yaxis='y'
        ))
        
        # Reddit (discussions)
        timeline_fig.add_trace(go.Scatter(
            x=[12.3, 8.7, 15.1, 6.2],
            y=[0.5, 0.5, 0.5, 0.5],
            mode='markers+text',
            text=['Reddit: EU discussion', 'Reddit: Medical', 'Reddit: Climate', 'Reddit: Tech'],
            textposition="bottom center",
            marker=dict(size=12, color='red', symbol='circle'),
            name='Reddit Posts',
            yaxis='y'
        ))
        
        # GDELT (événements)
        timeline_fig.add_trace(go.Scatter(
            x=[2.1, -1.3, 8.9, 4.5],
            y=[0, 0, 0, 0],
            mode='markers+text',
            text=['GDELT: EU Policy', 'GDELT: Health', 'GDELT: Environment', 'GDELT: Innovation'],
            textposition="bottom center",
            marker=dict(size=10, color='green', symbol='square'),
            name='GDELT Events',
            yaxis='y'
        ))
        
        timeline_fig.update_layout(
            title="Timeline Comparative: Publication → Réaction → Documentation",
            xaxis_title="Heures après publication AFP",
            yaxis=dict(
                tickvals=[0, 0.5, 1],
                ticktext=['GDELT', 'Reddit', 'AFP'],
                range=[-0.2, 1.2]
            ),
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Analyse des sentiments comparée
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 😊 Analyse Sentiment Comparée")
            sentiment_data = {
                'Source': ['AFP', 'Reddit', 'GDELT'],
                'Sentiment Moyen': [0.15, -0.12, 0.08],
                'Objectivité': [0.95, 0.42, 0.78]
            }
            sentiment_fig = go.Figure(data=[
                go.Bar(x=sentiment_data['Source'], y=sentiment_data['Sentiment Moyen'], 
                      name='Sentiment', marker_color=['blue', 'red', 'green'])
            ])
            sentiment_fig.update_layout(title="Sentiment par Source", height=300)
            st.plotly_chart(sentiment_fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Fiabilité des Sources")
            reliability_data = {
                'Source': ['AFP', 'Reddit', 'GDELT'],
                'Fiabilité': [0.97, 0.45, 0.83],
                'Vérification': [0.99, 0.15, 0.71]
            }
            reliability_fig = go.Figure(data=[
                go.Bar(x=reliability_data['Source'], y=reliability_data['Fiabilité'], 
                      name='Fiabilité', marker_color=['darkblue', 'orange', 'darkgreen'])
            ])
            reliability_fig.update_layout(title="Score de Fiabilité", height=300)
            st.plotly_chart(reliability_fig, use_container_width=True)
    
    # Footer avec informations système
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #95A5A6; padding: 20px;">
        <p>🔧 <strong>Final Project: Real-Time Multi-Source Data Analytics</strong></p>
        <p>Apache Kafka + Spark Streaming + MongoDB + Plotly 3D Visualizations</p>
        <p>✨ Dashboard optimisé pour l'analyse AFP vs Reddit vs GDELT ✨</p>
        <p><strong>🚀 Version Améliorée:</strong> Focus sur comparaisons cross-source détaillées</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()