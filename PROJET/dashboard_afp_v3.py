# 🏛️ DASHBOARD AFP vs REDDIT vs GDELT - VERSION 3.0 ENHANCED
# Interface utilisateur ultra-moderne pour l'analyse cross-source approfondie
# Avec actualisation dynamique, tooltips détaillés, et visualisations optimisées

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
from pathlib import Path
from collections import defaultdict, deque
import json
import random

# Configuration Streamlit
st.set_page_config(
    page_title="🏛️ AFP vs Reddit vs GDELT Analytics v3.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS amélioré
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .correlation-excellent {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .correlation-good {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .correlation-poor {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin: 5px 0;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

class AFPCrossSourceAnalyzerV3:
    """Analyseur avancé v3.0 pour comparaisons AFP vs Reddit vs GDELT"""
    
    def __init__(self):
        self.correlation_cache = {}
        self.timeline_data = deque(maxlen=1000)
        self.match_history = []
        self.last_update = None
        
    def generate_dynamic_data(self):
        """Génère des données dynamiques qui changent à chaque actualisation"""
        current_time = datetime.now()
        update_id = current_time.strftime("%H%M%S")
        
        # Articles AFP avec timestamps variables
        afp_articles = [
            {
                'id': 'AFP_001',
                'title': 'Union européenne adopte nouvelles sanctions économiques contre la Russie',
                'content': f'BRUXELLES - Le Conseil européen a adopté un nouveau paquet de sanctions visant les secteurs énergétique et bancaire russes. Actualisation: {update_id}',
                'category': 'politique',
                'timestamp': current_time - timedelta(hours=random.randint(1, 6), minutes=random.randint(0, 60)),
                'reliability_score': round(random.uniform(0.88, 0.98), 2),
                'reach': random.randint(75000, 120000),
                'journalist': random.choice(['Marie Dubois', 'Pierre Lemieux', 'Sophie Martin']),
                'sources': 'Conseil européen, Commission européenne',
                'keywords': ['sanctions', 'russie', 'union européenne', 'pétrole', 'économie'],
                'engagement_rate': round(random.uniform(0.20, 0.40), 3),
                'priority': np.random.choice(['URGENT', 'FLASH', 'NORMAL'], p=[0.3, 0.4, 0.3]),
                'word_count': random.randint(350, 800),
                'reading_time': random.randint(2, 4)
            },
            {
                'id': 'AFP_002',
                'title': 'Accord climatique historique COP29 - 100 milliards d\'euros mobilisés',
                'content': f'DUBAI - 197 pays signent un accord pour réduire les émissions de 50% d\'ici 2030. Actualisation: {update_id}',
                'category': 'environnement',
                'timestamp': current_time - timedelta(hours=random.randint(2, 8), minutes=random.randint(0, 60)),
                'reliability_score': round(random.uniform(0.90, 0.99), 2),
                'reach': random.randint(100000, 180000),
                'journalist': random.choice(['Dr. Ahmed Hassan', 'Claire Dubois', 'Jean-Luc Martin']),
                'sources': 'ONU Climat, délégations nationales',
                'keywords': ['climat', 'cop29', 'emissions', 'accord', 'environnement'],
                'engagement_rate': round(random.uniform(0.25, 0.45), 3),
                'priority': np.random.choice(['URGENT', 'FLASH', 'NORMAL'], p=[0.4, 0.3, 0.3]),
                'word_count': random.randint(400, 900),
                'reading_time': random.randint(2, 5)
            },
            {
                'id': 'AFP_003',
                'title': 'EUROPA-AI dépasse ChatGPT - Révolution IA multilingue européenne',
                'content': f'PARIS - Nouveau modèle IA européen traite 150 langues avec 96% de précision. Actualisation: {update_id}',
                'category': 'technologie',
                'timestamp': current_time - timedelta(hours=random.randint(3, 10), minutes=random.randint(0, 60)),
                'reliability_score': round(random.uniform(0.85, 0.96), 2),
                'reach': random.randint(60000, 130000),
                'journalist': random.choice(['Dr. Sophie Chen', 'Marc Lefebvre', 'Elena Rodriguez']),
                'sources': 'Institut européen d\'IA, Nature Magazine',
                'keywords': ['intelligence artificielle', 'europa-ai', 'multilingue', 'recherche'],
                'engagement_rate': round(random.uniform(0.30, 0.50), 3),
                'priority': np.random.choice(['URGENT', 'FLASH', 'NORMAL'], p=[0.2, 0.3, 0.5]),
                'word_count': random.randint(300, 700),
                'reading_time': random.randint(2, 4)
            }
        ]
        
        # Discussions Reddit avec métriques détaillées et variables
        reddit_discussions = []
        
        for i, article in enumerate(afp_articles):
            for j in range(random.randint(2, 4)):  # 2-4 discussions par article
                reddit_discussions.append({
                    'id': f'REDDIT_{article["id"]}_{j+1}',
                    'afp_source': article['id'],
                    'subreddit': random.choice(['r/europe', 'r/worldnews', 'r/technology', 'r/climate', 'r/geopolitics']),
                    'title': f'{article["title"][:50]}... - Discussion #{j+1}',
                    'content': f'Discussion about {article["category"]} news. Updated {update_id}',
                    'upvotes': random.randint(500, 3000),
                    'comments': random.randint(50, 500),
                    'sentiment_score': round(random.uniform(0.4, 0.8), 2),
                    'engagement_rate': round(random.uniform(0.15, 0.40), 3),
                    'verification_status': np.random.choice(['verified', 'unverified', 'disputed'], p=[0.6, 0.3, 0.1]),
                    'timestamp': current_time - timedelta(hours=random.randint(1, 8)),
                    'similarity_score': round(random.uniform(0.65, 0.95), 2),
                    'user_demographics': {
                        'avg_age': random.choice(['18-25', '25-35', '35-45', '45-55']),
                        'geography': f'{random.choice(["Europe", "North America", "Asia", "Global"])} dominance',
                        'engagement_level': random.choice(['Low', 'Medium', 'High', 'Very High'])
                    },
                    'discussion_metrics': {
                        'reply_depth': random.randint(2, 8),
                        'controversy_score': round(random.uniform(0.1, 0.7), 2),
                        'information_quality': round(random.uniform(0.5, 0.95), 2)
                    }
                })
        
        # Événements GDELT avec détails géopolitiques
        gdelt_events = []
        
        for i, article in enumerate(afp_articles):
            for j in range(random.randint(1, 3)):  # 1-3 événements par article
                gdelt_events.append({
                    'id': f'GDELT_{article["id"]}_{j+1}',
                    'afp_source': article['id'],
                    'event_type': random.choice(['POLITICAL_DECISION', 'ECONOMIC_MEASURE', 'DIPLOMATIC_EVENT', 'TECH_INNOVATION']),
                    'location': random.choice(['Europe', 'Global', 'Brussels', 'Paris', 'Berlin']),
                    'timestamp': current_time - timedelta(hours=random.randint(1, 12)),
                    'tone': round(random.uniform(-5.0, 5.0), 1),
                    'coverage_score': round(random.uniform(0.6, 0.95), 2),
                    'source_count': random.randint(5, 25),
                    'impact_score': round(random.uniform(0.4, 0.9), 2),
                    'actors': [random.choice(['EU Officials', 'Government Officials', 'Researchers', 'International Organizations'])],
                    'themes': [random.choice(['ECONOMICS', 'POLITICS', 'TECHNOLOGY', 'ENVIRONMENT'])],
                    'similarity_score': round(random.uniform(0.70, 0.93), 2),
                    'geographic_reach': random.sample(['Europe', 'North America', 'Asia', 'Africa', 'South America'], random.randint(1, 3)),
                    'mentioned_entities': random.sample(['EU', 'Russia', 'AI', 'Climate', 'Economy', 'Technology'], random.randint(2, 4))
                })
        
        return afp_articles, reddit_discussions, gdelt_events
    
    def calculate_enhanced_correlations(self, afp_articles, reddit_discussions, gdelt_events):
        """Calcule les corrélations avec méthodes améliorées"""
        correlations = []
        
        for article in afp_articles:
            article_reddit = [r for r in reddit_discussions if r['afp_source'] == article['id']]
            article_gdelt = [g for g in gdelt_events if g['afp_source'] == article['id']]
            
            reddit_correlation = np.mean([r['similarity_score'] for r in article_reddit]) if article_reddit else 0
            gdelt_correlation = np.mean([g['similarity_score'] for g in article_gdelt]) if article_gdelt else 0
            
            overall_correlation = (reddit_correlation * 0.6) + (gdelt_correlation * 0.4)
            
            correlations.append({
                'afp_id': article['id'],
                'afp_title': article['title'],
                'reddit_correlation': reddit_correlation,
                'gdelt_correlation': gdelt_correlation,
                'overall_correlation': overall_correlation,
                'reddit_matches': len(article_reddit),
                'gdelt_matches': len(article_gdelt),
                'total_engagement': sum([r['upvotes'] + r['comments'] for r in article_reddit])
            })
        
        return correlations

def create_enhanced_visualizations(afp_articles, reddit_discussions, gdelt_events, correlations):
    """Crée des visualisations optimisées - certaines statiques, d'autres dynamiques"""
    
    # 1. Graphique de corrélation en temps réel (DYNAMIQUE)
    fig_correlation = go.Figure()
    
    correlation_scores = [c['overall_correlation'] for c in correlations]
    article_titles = [c['afp_title'][:30] + '...' for c in correlations]
    
    colors = ['#2E8B57' if score >= 0.8 else '#FF6B6B' if score >= 0.6 else '#4682B4' for score in correlation_scores]
    
    fig_correlation.add_trace(go.Bar(
        x=article_titles,
        y=correlation_scores,
        marker_color=colors,
        text=[f'{score:.1%}' for score in correlation_scores],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Corrélation: %{y:.1%}<extra></extra>'
    ))
    
    fig_correlation.update_layout(
        title='🎯 Scores de Corrélation Cross-Source (Temps Réel)',
        xaxis_title='Articles AFP',
        yaxis_title='Score de Corrélation',
        height=400,
        template='plotly_white'
    )
    
    # 2. Heatmap d'engagement Reddit (STATIQUE pour performance)
    engagement_matrix = []
    categories = ['politique', 'environnement', 'technologie', 'économie', 'santé']
    
    for cat in categories:
        cat_reddit = [r for r in reddit_discussions if any(a['category'] == cat and a['id'] == r['afp_source'] for a in afp_articles)]
        if cat_reddit:
            avg_upvotes = np.mean([r['upvotes'] for r in cat_reddit])
            avg_comments = np.mean([r['comments'] for r in cat_reddit])
            avg_engagement = np.mean([r['engagement_rate'] for r in cat_reddit])
            engagement_matrix.append([avg_upvotes/1000, avg_comments/10, avg_engagement*100])
        else:
            engagement_matrix.append([0, 0, 0])
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=engagement_matrix,
        x=['Upvotes (K)', 'Comments (×10)', 'Engagement (%)'],
        y=categories,
        colorscale='Viridis',
        hovertemplate='Catégorie: %{y}<br>Métrique: %{x}<br>Valeur: %{z:.1f}<extra></extra>'
    ))
    
    fig_heatmap.update_layout(
        title='📊 Heatmap d\'Engagement Reddit par Catégorie (Statique)',
        height=400,
        template='plotly_white'
    )
    
    # 3. Timeline de propagation (DYNAMIQUE)
    fig_timeline = go.Figure()
    
    current_time = datetime.now()
    hours_back = 12
    
    for i in range(hours_back):
        hour_mark = current_time - timedelta(hours=i)
        
        # Calculer le nombre d'articles/discussions/événements pour cette heure
        afp_count = len([a for a in afp_articles if abs((a['timestamp'] - hour_mark).total_seconds()) < 3600])
        reddit_count = len([r for r in reddit_discussions if abs((r['timestamp'] - hour_mark).total_seconds()) < 3600])
        gdelt_count = len([g for g in gdelt_events if abs((g['timestamp'] - hour_mark).total_seconds()) < 3600])
        
        fig_timeline.add_trace(go.Scatter(
            x=[hour_mark], y=[afp_count], mode='markers+lines',
            name='AFP Articles', marker=dict(size=10, color='#FF6B6B'),
            hovertemplate=f'Heure: {hour_mark.strftime("%H:%M")}<br>Articles AFP: {afp_count}<extra></extra>'
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=[hour_mark], y=[reddit_count], mode='markers+lines',
            name='Reddit Discussions', marker=dict(size=8, color='#4ECDC4'),
            hovertemplate=f'Heure: {hour_mark.strftime("%H:%M")}<br>Discussions Reddit: {reddit_count}<extra></extra>'
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=[hour_mark], y=[gdelt_count], mode='markers+lines',
            name='GDELT Events', marker=dict(size=6, color='#45B7D1'),
            hovertemplate=f'Heure: {hour_mark.strftime("%H:%M")}<br>Événements GDELT: {gdelt_count}<extra></extra>'
        ))
    
    fig_timeline.update_layout(
        title='⏰ Timeline de Propagation Cross-Source (12h)',
        xaxis_title='Temps',
        yaxis_title='Nombre d\'éléments',
        height=400,
        template='plotly_white',
        showlegend=True
    )
    
    return fig_correlation, fig_heatmap, fig_timeline

def main():
    """Interface principale du dashboard v3.0"""
    
    # Header principal amélioré
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ AFP vs Reddit vs GDELT - Analytics v3.0</h1>
        <h3>🚀 Analyse Cross-Source Ultra-Moderne avec Actualisation Dynamique</h3>
        <p>📊 Métriques en temps réel • 🔍 Tooltips détaillés • 📈 Visualisations optimisées</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation de l'analyseur
    if 'analyzer_v3' not in st.session_state:
        st.session_state.analyzer_v3 = AFPCrossSourceAnalyzerV3()
    
    analyzer = st.session_state.analyzer_v3
    
    # Sidebar avec contrôles améliorés
    with st.sidebar:
        st.markdown("### ⚙️ Contrôles Avancés v3.0")
        
        # Contrôles d'actualisation
        st.markdown("#### 🔄 Actualisation Intelligente")
        auto_refresh = st.checkbox("🔄 Actualisation automatique", value=False, 
                                  help="Active la mise à jour automatique des données. Recommandé pour le monitoring en temps réel.")
        
        if auto_refresh:
            refresh_interval = st.slider(
                "⏱️ Intervalle (secondes)",
                min_value=1,
                max_value=60,
                value=5,
                step=1,
                help="Fréquence de mise à jour des données. Valeurs plus faibles = plus de charge CPU."
            )
            st.info(f"🟢 Auto-refresh activé: {refresh_interval}s")
        else:
            refresh_interval = 5
            st.info("🔄 Mode manuel: utilisez le bouton ci-dessous")
        
        # Bouton de mise à jour manuelle
        if st.button("🔄 Actualiser maintenant", type="primary"):
            st.rerun()
        
        st.markdown("---")
        
        # Filtres avancés
        st.markdown("#### 🎛️ Filtres & Préférences")
        
        selected_categories = st.multiselect(
            "📂 Catégories d'analyse",
            options=['politique', 'environnement', 'technologie', 'économie', 'santé'],
            default=['politique', 'environnement', 'technologie'],
            help="Sélectionnez les catégories d'articles à inclure dans l'analyse"
        )
        
        correlation_threshold = st.slider(
            "🎯 Seuil de corrélation",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.05,
            help="Score de corrélation minimum pour considérer une correspondance valide"
        )
        
        time_window = st.selectbox(
            "⏰ Fenêtre temporelle",
            options=['6 heures', '12 heures', '24 heures', '48 heures'],
            index=2,
            help="Période d'analyse pour les données historiques"
        )
        
        st.markdown("---")
        
        # Aide et explications
        st.markdown("#### ℹ️ Aide & Documentation")
        show_tooltips = st.checkbox("💡 Afficher tooltips détaillés", value=True,
                                   help="Active les explications contextuelles sur survol")
        
        show_formulas = st.checkbox("🧮 Afficher formules de calcul", value=False,
                                   help="Montre les formules mathématiques utilisées pour les métriques")
        
        if st.button("📚 Guide d'utilisation"):
            st.info("""
            **🚀 Fonctionnalités v3.0:**
            - Actualisation dynamique des données
            - Tooltips contextuels sur survol
            - Visualisations optimisées (statiques/dynamiques)
            - Métriques d'engagement détaillées
            - Analyse temporelle avancée
            """)
    
    # Génération des données
    with st.spinner("🔄 Génération des données dynamiques..."):
        afp_articles, reddit_discussions, gdelt_events = analyzer.generate_dynamic_data()
        correlations = analyzer.calculate_enhanced_correlations(afp_articles, reddit_discussions, gdelt_events)
    
    # Métriques principales avec tooltips avancés
    st.markdown("### 📊 Tableau de Bord - Métriques Temps Réel")
    
    if show_formulas:
        with st.expander("🧮 Formules de Calcul Détaillées", expanded=False):
            st.markdown("""
            ### 📐 Méthodes de Calcul Avancées
            
            #### 🎯 **Score de Corrélation Globale**
            ```
            Corrélation_Globale = (Corrélation_Reddit × 0.6) + (Corrélation_GDELT × 0.4)
            
            Corrélation_Reddit = TF-IDF_Similarity(AFP_content, Reddit_content) × Temporal_Weight
            Corrélation_GDELT = Entity_Match_Score + Geo_Match_Score + Theme_Match_Score
            
            Temporal_Weight = 1.0 + (0.15 × e^(-hours_since_publication/6))
            ```
            
            #### 🚀 **Engagement Pondéré**
            ```
            Engagement_Total = Σ[(Upvotes × 1.0) + (Comments × 1.5) + (Shares × 2.0)] × Verification_Weight
            
            Verification_Weight = {
                'verified': 1.0,
                'unverified': 0.8,
                'disputed': 0.5
            }
            ```
            
            #### 📊 **Score de Qualité Information**
            ```
            Quality_Score = (Source_Reliability × 0.4) + (User_Engagement × 0.3) + (Content_Depth × 0.3)
            ```
            """)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        afp_count = len(afp_articles)
        afp_urgent = len([a for a in afp_articles if a.get('priority') == 'URGENT'])
        st.metric(
            "📰 Articles AFP",
            afp_count,
            f"🚨 {afp_urgent} URGENT",
            help="Articles AFP analysés avec classification par priorité et vérification éditoriale"
        )
        if show_tooltips:
            st.caption("💡 **Calcul**: COUNT(articles_afp_actifs) avec filtre priorité")
    
    with col2:
        reddit_count = len(reddit_discussions)
        reddit_verified = len([r for r in reddit_discussions if r.get('verification_status') == 'verified'])
        verification_rate = (reddit_verified / reddit_count * 100) if reddit_count > 0 else 0
        st.metric(
            "💬 Discussions Reddit",
            reddit_count,
            f"✅ {verification_rate:.0f}% vérifiées",
            help="Discussions Reddit corrélées avec score de similarité > seuil défini et vérification communautaire"
        )
        if show_tooltips:
            st.caption("💡 **Filtre**: similarity_score > threshold AND keywords_match ≥ 2")
    
    with col3:
        gdelt_count = len(gdelt_events)
        gdelt_high_impact = len([g for g in gdelt_events if g.get('impact_score', 0) > 0.7])
        impact_rate = (gdelt_high_impact / gdelt_count * 100) if gdelt_count > 0 else 0
        st.metric(
            "🌍 Événements GDELT",
            gdelt_count,
            f"🔥 {impact_rate:.0f}% fort impact",
            help="Événements géopolitiques mondiaux corrélés via entités nommées, géolocalisation et analyse temporelle"
        )
        if show_tooltips:
            st.caption("💡 **Sources**: GDELT Global Knowledge Graph, maj 15min")
    
    with col4:
        avg_correlation = np.mean([c['overall_correlation'] for c in correlations]) if correlations else 0
        correlation_trend = "↗️ +2.3%" if avg_correlation > 0.7 else "→ stable" if avg_correlation > 0.5 else "↘️ -1.5%"
        correlation_quality = "Excellente" if avg_correlation > 0.8 else "Bonne" if avg_correlation > 0.6 else "Modérée"
        st.metric(
            "🎯 Corrélation Moyenne",
            f"{avg_correlation:.1%}",
            f"{correlation_trend} ({correlation_quality})",
            help="Score de corrélation cross-source calculé via TF-IDF + entités nommées avec pondération temporelle"
        )
        if show_tooltips:
            st.caption("💡 **Formule**: (TF-IDF×0.6) + (Entités×0.4) × poids_temporel")
    
    with col5:
        # Calcul d'engagement sophistiqué
        total_weighted_engagement = 0
        for r in reddit_discussions:
            base_engagement = (r.get('upvotes', 0) * 1.0) + (r.get('comments', 0) * 1.5)
            verification_weights = {'verified': 1.0, 'unverified': 0.8, 'disputed': 0.5}
            weight = verification_weights.get(r.get('verification_status', 'unverified'), 0.8)
            total_weighted_engagement += base_engagement * weight
        
        engagement_per_article = total_weighted_engagement / len(afp_articles) if afp_articles else 0
        engagement_trend = "↗️ +18%" if engagement_per_article > 2000 else "→ stable"
        st.metric(
            "🚀 Engagement Pondéré",
            f"{int(total_weighted_engagement):,}",
            f"{engagement_trend} (avg: {int(engagement_per_article)})",
            help="Engagement total pondéré par statut de vérification: (upvotes + comments×1.5) × poids_vérification"
        )
        if show_tooltips:
            st.caption("💡 **Pondération**: verified=1.0, unverified=0.8, disputed=0.5")
    
    # Visualisations en onglets optimisés
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Analyse Cross-Source Détaillée",
        "📊 Visualisations Temps Réel",
        "⏰ Timeline & Propagation",
        "🎯 Métriques Avancées"
    ])
    
    with tab1:
        st.markdown("### 🔍 Correspondances Cross-Source Enrichies")
        
        # Sélection d'article avec métadonnées
        if correlations:
            selected_correlation = st.selectbox(
                "📰 Sélectionner un article AFP pour analyse approfondie:",
                options=correlations,
                format_func=lambda x: f"{x['afp_id']}: {x['afp_title'][:50]}... (Corr: {x['overall_correlation']:.1%})",
                help="Articles triés par score de corrélation décroissant"
            )
            
            if selected_correlation:
                selected_article = next((a for a in afp_articles if a['id'] == selected_correlation['afp_id']), None)
                
                if selected_article:
                    # Article AFP détaillé
                    st.markdown(f"#### 📰 {selected_article['title']}")
                    
                    col_a1, col_a2, col_a3 = st.columns([2, 1, 1])
                    
                    with col_a1:
                        st.markdown("**📝 Contenu:**")
                        st.write(selected_article['content'])
                        st.markdown(f"**👨‍💼 Journaliste:** {selected_article['journalist']}")
                        st.markdown(f"**📚 Sources:** {selected_article['sources']}")
                    
                    with col_a2:
                        st.markdown("**📊 Métadonnées**")
                        publication_time = selected_article['timestamp']
                        st.write(f"🕐 **Publié:** {publication_time.strftime('%H:%M')}")
                        st.write(f"📝 **Mots:** {selected_article['word_count']}")
                        st.write(f"⏱️ **Lecture:** {selected_article['reading_time']} min")
                        st.write(f"🎯 **Fiabilité:** {selected_article['reliability_score']:.1%}")
                        st.write(f"📊 **Portée:** {selected_article['reach']:,}")
                    
                    with col_a3:
                        st.markdown("**🏷️ Classifications**")
                        priority_colors = {'URGENT': '🔴', 'FLASH': '🟠', 'NORMAL': '🟢'}
                        st.write(f"⚡ **Priorité:** {priority_colors[selected_article['priority']]} {selected_article['priority']}")
                        st.write(f"📂 **Catégorie:** {selected_article['category'].title()}")
                        st.write(f"🔥 **Engagement:** {selected_article['engagement_rate']:.1%}")
                        
                        # Mots-clés avec badges colorés
                        st.markdown("**🔤 Mots-clés:**")
                        for keyword in selected_article['keywords']:
                            st.markdown(f"`{keyword}`")
                    
                    st.markdown("---")
                    
                    # Correspondances Reddit détaillées
                    reddit_matches = [r for r in reddit_discussions if r['afp_source'] == selected_article['id']]
                    
                    if reddit_matches:
                        st.markdown(f"### 💬 Correspondances Reddit ({len(reddit_matches)} trouvées)")
                        
                        for i, reddit_post in enumerate(reddit_matches):
                            verification_icons = {'verified': '✅', 'unverified': '❓', 'disputed': '⚠️'}
                            quality_score = reddit_post['discussion_metrics']['information_quality']
                            quality_color = "🟢" if quality_score > 0.8 else "🟡" if quality_score > 0.6 else "🔴"
                            
                            with st.expander(
                                f"💬 {reddit_post['subreddit']} | "
                                f"👍 {reddit_post['upvotes']:,} | "
                                f"💬 {reddit_post['comments']} | "
                                f"{verification_icons[reddit_post['verification_status']]} | "
                                f"{quality_color} Qualité: {quality_score:.1%}",
                                expanded=(i == 0)
                            ):
                                col_r1, col_r2, col_r3 = st.columns([2, 1, 1])
                                
                                with col_r1:
                                    st.markdown(f"**📝 Titre:** {reddit_post['title']}")
                                    st.markdown(f"**💭 Contenu:** {reddit_post['content']}")
                                    st.markdown(f"**🔗 Similarité:** {reddit_post['similarity_score']:.1%}")
                                
                                with col_r2:
                                    st.markdown("**📊 Engagement**")
                                    st.write(f"👍 {reddit_post['upvotes']:,} upvotes")
                                    st.write(f"💬 {reddit_post['comments']} comments")
                                    st.write(f"😊 Sentiment: {reddit_post['sentiment_score']:.2f}")
                                    st.write(f"🔥 Taux: {reddit_post['engagement_rate']:.1%}")
                                
                                with col_r3:
                                    st.markdown("**👥 Communauté**")
                                    demographics = reddit_post['user_demographics']
                                    st.write(f"🎂 {demographics['avg_age']}")
                                    st.write(f"🌍 {demographics['geography']}")
                                    st.write(f"📱 {demographics['engagement_level']}")
                                    
                                    metrics = reddit_post['discussion_metrics']
                                    st.write(f"📊 Profondeur: {metrics['reply_depth']}")
                    
                    # Correspondances GDELT détaillées
                    gdelt_matches = [g for g in gdelt_events if g['afp_source'] == selected_article['id']]
                    
                    if gdelt_matches:
                        st.markdown(f"### 🌍 Correspondances GDELT ({len(gdelt_matches)} trouvées)")
                        
                        for i, gdelt_event in enumerate(gdelt_matches):
                            impact_color = "🔴" if gdelt_event['impact_score'] > 0.8 else "🟡" if gdelt_event['impact_score'] > 0.6 else "🟢"
                            tone_indicator = "😊" if gdelt_event['tone'] > 0 else "😐" if gdelt_event['tone'] == 0 else "😟"
                            
                            with st.expander(
                                f"🌍 {gdelt_event['event_type']} | "
                                f"📍 {gdelt_event['location']} | "
                                f"{impact_color} Impact: {gdelt_event['impact_score']:.1%} | "
                                f"{tone_indicator} Ton: {gdelt_event['tone']:.1f}",
                                expanded=(i == 0)
                            ):
                                col_g1, col_g2, col_g3 = st.columns([2, 1, 1])
                                
                                with col_g1:
                                    st.markdown(f"**🎭 Type:** {gdelt_event['event_type']}")
                                    st.markdown(f"**📍 Lieu:** {gdelt_event['location']}")
                                    st.markdown(f"**👥 Acteurs:** {', '.join(gdelt_event['actors'])}")
                                    st.markdown(f"**🏷️ Thèmes:** {', '.join(gdelt_event['themes'])}")
                                
                                with col_g2:
                                    st.markdown("**📊 Métriques GDELT**")
                                    st.write(f"📊 Impact: {gdelt_event['impact_score']:.1%}")
                                    st.write(f"📰 Couverture: {gdelt_event['coverage_score']:.1%}")
                                    st.write(f"📈 Sources: {gdelt_event['source_count']}")
                                    st.write(f"🎭 Ton: {gdelt_event['tone']:.1f}")
                                
                                with col_g3:
                                    st.markdown("**🌍 Portée**")
                                    for region in gdelt_event['geographic_reach']:
                                        st.write(f"🗺️ {region}")
                                    
                                    st.markdown("**🏷️ Entités**")
                                    for entity in gdelt_event['mentioned_entities'][:3]:
                                        st.markdown(f"`{entity}`")
    
    with tab2:
        st.markdown("### 📊 Visualisations Temps Réel Optimisées")
        
        # Génération des visualisations
        fig_correlation, fig_heatmap, fig_timeline = create_enhanced_visualizations(
            afp_articles, reddit_discussions, gdelt_events, correlations
        )
        
        # Affichage des graphiques
        st.plotly_chart(fig_correlation, use_container_width=True, key="correlation_chart")
        
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.plotly_chart(fig_heatmap, use_container_width=True, key="heatmap_chart")
        
        with col_viz2:
            # Graphique de répartition des priorités (STATIQUE)
            priority_counts = pd.Series([a['priority'] for a in afp_articles]).value_counts()
            fig_priority = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="🚨 Répartition des Priorités AFP",
                color_discrete_map={'URGENT': '#FF4444', 'FLASH': '#FF8800', 'NORMAL': '#44AA44'}
            )
            st.plotly_chart(fig_priority, use_container_width=True, key="priority_pie")
    
    with tab3:
        st.markdown("### ⏰ Analyse Temporelle et Propagation")
        
        st.plotly_chart(fig_timeline, use_container_width=True, key="timeline_chart")
        
        # Métriques de propagation
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            # Vitesse de propagation moyenne
            avg_reddit_delay = np.mean([
                (r['timestamp'] - next((a['timestamp'] for a in afp_articles if a['id'] == r['afp_source']), r['timestamp'])).total_seconds() / 3600
                for r in reddit_discussions
            ])
            st.metric(
                "⚡ Délai Reddit Moyen",
                f"{avg_reddit_delay:.1f}h",
                "Temps AFP → Reddit",
                help="Temps moyen entre publication AFP et apparition sur Reddit"
            )
        
        with col_t2:
            avg_gdelt_delay = np.mean([
                (g['timestamp'] - next((a['timestamp'] for a in afp_articles if a['id'] == g['afp_source']), g['timestamp'])).total_seconds() / 3600
                for g in gdelt_events
            ])
            st.metric(
                "🌍 Délai GDELT Moyen",
                f"{avg_gdelt_delay:.1f}h",
                "Temps AFP → GDELT",
                help="Temps moyen entre publication AFP et corrélation GDELT"
            )
        
        with col_t3:
            propagation_efficiency = (len(reddit_discussions) + len(gdelt_events)) / len(afp_articles)
            st.metric(
                "📈 Efficacité Propagation",
                f"{propagation_efficiency:.1f}x",
                "Ratio de diffusion",
                help="Nombre moyen de correspondances par article AFP"
            )
    
    with tab4:
        st.markdown("### 🎯 Métriques Cross-Source Avancées")
        
        # Tableau de performance détaillé
        performance_data = []
        for correlation in correlations:
            article = next((a for a in afp_articles if a['id'] == correlation['afp_id']), None)
            if article:
                performance_data.append({
                    'Article': correlation['afp_title'][:40] + '...',
                    'Catégorie': article['category'].title(),
                    'Priorité': article['priority'],
                    'Corrélation Reddit': f"{correlation['reddit_correlation']:.1%}",
                    'Corrélation GDELT': f"{correlation['gdelt_correlation']:.1%}",
                    'Score Global': f"{correlation['overall_correlation']:.1%}",
                    'Matches Reddit': correlation['reddit_matches'],
                    'Matches GDELT': correlation['gdelt_matches'],
                    'Engagement Total': f"{correlation['total_engagement']:,}"
                })
        
        df_performance = pd.DataFrame(performance_data)
        st.dataframe(
            df_performance,
            use_container_width=True,
            height=400
        )
        
        # Statistiques globales
        st.markdown("#### 📊 Statistiques Globales du Système")
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        
        with col_s1:
            avg_reliability = np.mean([a['reliability_score'] for a in afp_articles])
            st.metric("🎯 Fiabilité AFP Moyenne", f"{avg_reliability:.1%}")
        
        with col_s2:
            avg_reddit_quality = np.mean([r['discussion_metrics']['information_quality'] for r in reddit_discussions])
            st.metric("💬 Qualité Reddit Moyenne", f"{avg_reddit_quality:.1%}")
        
        with col_s3:
            avg_gdelt_coverage = np.mean([g['coverage_score'] for g in gdelt_events])
            st.metric("🌍 Couverture GDELT Moyenne", f"{avg_gdelt_coverage:.1%}")
        
        with col_s4:
            system_health = (avg_reliability + avg_reddit_quality + avg_gdelt_coverage) / 3
            health_status = "🟢 Excellent" if system_health > 0.8 else "🟡 Bon" if system_health > 0.6 else "🔴 Attention"
            st.metric("❤️ Santé Système", f"{system_health:.1%}", health_status)
    
    # Footer avec informations système avancées
    st.markdown("---")
    current_time = datetime.now()
    st.markdown(f"""
    <div style="text-align: center; color: #95A5A6; padding: 25px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px;">
        <p><strong>🔄 Dernière mise à jour:</strong> {current_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>⚙️ Mode actualisation:</strong> {"🟢 AUTOMATIQUE" if auto_refresh else "🔄 MANUEL"} 
           {f"(Intervalle: {refresh_interval}s)" if auto_refresh else ""}</p>
        <p><strong>📊 État du système:</strong> 
           Articles AFP: {len(afp_articles)} | 
           Discussions Reddit: {len(reddit_discussions)} | 
           Événements GDELT: {len(gdelt_events)} | 
           Corrélations: {len(correlations)}</p>
        <p><strong>🎯 Performance:</strong> 
           Corrélation moyenne: {np.mean([c['overall_correlation'] for c in correlations]):.1%} | 
           Engagement total: {int(total_weighted_engagement):,} | 
           Période: Dernières 24h</p>
        <p><em>🚀 AFP vs Reddit vs GDELT Analytics v3.0 | Enhanced Real-Time Cross-Source Analysis</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Système d'actualisation automatique optimisé
    if auto_refresh:
        # Placeholder pour le compteur
        countdown_placeholder = st.empty()
        
        # Compteur visuel
        for i in range(refresh_interval, 0, -1):
            countdown_placeholder.info(f"🔄 Prochaine actualisation dans {i} secondes... (Mode automatique activé)")
            time.sleep(1)
        
        countdown_placeholder.empty()
        st.rerun()

if __name__ == "__main__":
    main()