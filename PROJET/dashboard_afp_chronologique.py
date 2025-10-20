# 🏛️ DASHBOARD AFP CHRONOLOGIQUE - VERSION CORRIGÉE
# Interface avec dates fixes et liste chronologique des news AFP
# Correction des timestamps qui changeaient à chaque actualisation

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from pathlib import Path
import json
import hashlib

# Configuration Streamlit
st.set_page_config(
    page_title="🏛️ AFP News Timeline - Dates Fixes",
    page_icon="📰",
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
    .news-item {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .timestamp-fixed {
        background: linear-gradient(135deg, #2ECC71, #27AE60);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        display: inline-block;
        margin: 5px 0;
    }
    .priority-urgent {
        background: linear-gradient(135deg, #FF6B6B, #FF4757);
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .priority-flash {
        background: linear-gradient(135deg, #FFA502, #FF6348);
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .priority-normal {
        background: linear-gradient(135deg, #70A1FF, #5352ED);
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .category-tag {
        background: linear-gradient(135deg, #A55EEA, #26C6DA);
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75em;
        margin: 2px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

class AFPNewsManager:
    """Gestionnaire des news AFP avec dates fixes et liste chronologique"""
    
    def __init__(self):
        self.cache_file = Path("afp_news_cache.json")
        self.news_data = self._load_or_create_news()
        
    def _load_or_create_news(self):
        """Charge les news depuis le cache ou les crée avec des dates fixes"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convertir les timestamps string en datetime
                for article in data:
                    article['publication_date'] = datetime.fromisoformat(article['publication_date'])
                    article['last_update'] = datetime.fromisoformat(article['last_update'])
                return data
        else:
            return self._create_fixed_news_data()
    
    def _create_fixed_news_data(self):
        """Crée des données d'articles AFP avec dates fixes"""
        base_time = datetime.now()
        
        # Articles avec des dates fixes qui ne changeront plus
        fixed_articles = [
            {
                'id': 'AFP_001',
                'title': 'UE adopte nouvelles sanctions contre Russie - Embargo pétrolier renforcé',
                'content': 'BRUXELLES - Le Conseil européen a approuvé un 12e paquet de sanctions contre la Russie, incluant un embargo total sur le pétrole russe et de nouvelles restrictions bancaires. Ces mesures entrent en vigueur immédiatement.',
                'category': 'politique',
                'publication_date': base_time - timedelta(hours=2, minutes=15),
                'last_update': base_time - timedelta(hours=1, minutes=45),
                'journalist': 'Marie Dubois',
                'sources': 'Conseil européen, Commission européenne',
                'keywords': ['sanctions', 'russie', 'union européenne', 'pétrole', 'embargo'],
                'priority': 'URGENT',
                'reliability_score': 0.98,
                'reach': 125000,
                'word_count': 456,
                'reading_time': 2,
                'engagement_rate': 0.34,
                'location': 'Bruxelles, Belgique'
            },
            {
                'id': 'AFP_002',
                'title': 'COP29 Dubai - Accord historique 100 milliards pour le climat',
                'content': 'DUBAI - Les 197 pays participants à la COP29 ont signé un accord historique prévoyant 100 milliards d\'euros pour lutter contre le changement climatique. L\'objectif est de réduire les émissions de 50% d\'ici 2030.',
                'category': 'environnement',
                'publication_date': base_time - timedelta(hours=4, minutes=30),
                'last_update': base_time - timedelta(hours=3, minutes=55),
                'journalist': 'Pierre Martin',
                'sources': 'ONU Climat, délégations nationales',
                'keywords': ['climat', 'cop29', 'emissions', 'accord', 'environnement'],
                'priority': 'FLASH',
                'reliability_score': 0.97,
                'reach': 180000,
                'word_count': 523,
                'reading_time': 3,
                'engagement_rate': 0.42,
                'location': 'Dubai, Émirats Arabes Unis'
            },
            {
                'id': 'AFP_003',
                'title': 'EUROPA-AI révolutionne l\'IA - 150 langues maîtrisées à 96%',
                'content': 'PARIS - Une équipe de chercheurs européens dévoile EUROPA-AI, un modèle d\'intelligence artificielle capable de traiter 150 langues avec une précision de 96%. Cette avancée majeure dépasse les performances de ChatGPT.',
                'category': 'technologie',
                'publication_date': base_time - timedelta(hours=6, minutes=45),
                'last_update': base_time - timedelta(hours=5, minutes=20),
                'journalist': 'Dr. Sophie Chen',
                'sources': 'Institut européen d\'IA, Nature Magazine',
                'keywords': ['intelligence artificielle', 'europa-ai', 'multilingue', 'recherche'],
                'priority': 'NORMAL',
                'reliability_score': 0.95,
                'reach': 95000,
                'word_count': 389,
                'reading_time': 2,
                'engagement_rate': 0.38,
                'location': 'Paris, France'
            },
            {
                'id': 'AFP_004',
                'title': 'OMS évite nouvelle pandémie grâce au système d\'alerte précoce',
                'content': 'GENÈVE - L\'Organisation mondiale de la santé annonce avoir détecté et contenu un nouveau virus en Asie du Sud-Est avant sa propagation internationale. Le système d\'alerte précoce a fonctionné parfaitement.',
                'category': 'santé',
                'publication_date': base_time - timedelta(hours=8, minutes=20),
                'last_update': base_time - timedelta(hours=7, minutes=45),
                'journalist': 'Dr. Ahmed Hassan',
                'sources': 'OMS, ministères de la santé nationaux',
                'keywords': ['pandémie', 'oms', 'virus', 'alerte précoce', 'santé'],
                'priority': 'URGENT',
                'reliability_score': 0.99,
                'reach': 220000,
                'word_count': 445,
                'reading_time': 2,
                'engagement_rate': 0.45,
                'location': 'Genève, Suisse'
            },
            {
                'id': 'AFP_005',
                'title': 'BCE réforme système bancaire européen - Nouvelles règles prudentielles',
                'content': 'FRANCFORT - La Banque centrale européenne met en place de nouvelles règles prudentielles pour renforcer la stabilité financière. Ces mesures visent à prévenir les crises futures.',
                'category': 'économie',
                'publication_date': base_time - timedelta(hours=10, minutes=35),
                'last_update': base_time - timedelta(hours=9, minutes=10),
                'journalist': 'François Leclerc',
                'sources': 'BCE, banques centrales nationales',
                'keywords': ['bce', 'bancaire', 'réforme', 'prudentiel', 'stabilité'],
                'priority': 'NORMAL',
                'reliability_score': 0.96,
                'reach': 75000,
                'word_count': 367,
                'reading_time': 2,
                'engagement_rate': 0.28,
                'location': 'Francfort, Allemagne'
            },
            {
                'id': 'AFP_006',
                'title': 'France annonce plan hydrogène vert - 10 milliards d\'investissement',
                'content': 'PARIS - Le gouvernement français dévoile un plan massif de 10 milliards d\'euros pour développer l\'hydrogène vert. L\'objectif est de créer 100 000 emplois d\'ici 2030.',
                'category': 'environnement',
                'publication_date': base_time - timedelta(hours=12, minutes=50),
                'last_update': base_time - timedelta(hours=11, minutes=25),
                'journalist': 'Claire Dubois',
                'sources': 'Ministère de la Transition écologique',
                'keywords': ['hydrogène', 'vert', 'investissement', 'emplois', 'transition'],
                'priority': 'FLASH',
                'reliability_score': 0.94,
                'reach': 110000,
                'word_count': 412,
                'reading_time': 2,
                'engagement_rate': 0.31,
                'location': 'Paris, France'
            },
            {
                'id': 'AFP_007',
                'title': 'Élections européennes 2024 - Forte participation attendue',
                'content': 'BRUXELLES - Les derniers sondages indiquent une participation record attendue pour les élections européennes. Les enjeux climatiques et géopolitiques mobilisent les électeurs.',
                'category': 'politique',
                'publication_date': base_time - timedelta(hours=14, minutes=15),
                'last_update': base_time - timedelta(hours=13, minutes=40),
                'journalist': 'Jean-Luc Martin',
                'sources': 'Parlement européen, instituts de sondage',
                'keywords': ['élections', 'européennes', 'participation', 'sondages', 'mobilisation'],
                'priority': 'NORMAL',
                'reliability_score': 0.92,
                'reach': 65000,
                'word_count': 334,
                'reading_time': 2,
                'engagement_rate': 0.26,
                'location': 'Bruxelles, Belgique'
            },
            {
                'id': 'AFP_008',
                'title': 'Découverte médicale majeure - Nouveau traitement Alzheimer',
                'content': 'STOCKHOLM - Des chercheurs suédois annoncent une percée dans le traitement de la maladie d\'Alzheimer. Les premiers essais cliniques montrent une efficacité de 85%.',
                'category': 'santé',
                'publication_date': base_time - timedelta(hours=16, minutes=40),
                'last_update': base_time - timedelta(hours=15, minutes=55),
                'journalist': 'Dr. Elena Rodriguez',
                'sources': 'Institut Karolinska, revue Nature Medicine',
                'keywords': ['alzheimer', 'traitement', 'recherche', 'médicale', 'essais'],
                'priority': 'FLASH',
                'reliability_score': 0.97,
                'reach': 145000,
                'word_count': 478,
                'reading_time': 3,
                'engagement_rate': 0.41,
                'location': 'Stockholm, Suède'
            },
            {
                'id': 'AFP_009',
                'title': 'Quantum Computing - Première percée commerciale européenne',
                'content': 'MUNICH - Une startup allemande annonce le premier ordinateur quantique commercial européen. Cette technologie révolutionnaire promet de transformer le calcul scientifique.',
                'category': 'technologie',
                'publication_date': base_time - timedelta(hours=18, minutes=25),
                'last_update': base_time - timedelta(hours=17, minutes=50),
                'journalist': 'Marc Lefebvre',
                'sources': 'Université technique de Munich, startup QuantumEU',
                'keywords': ['quantum', 'computing', 'commercial', 'technologie', 'calcul'],
                'priority': 'NORMAL',
                'reliability_score': 0.93,
                'reach': 85000,
                'word_count': 356,
                'reading_time': 2,
                'engagement_rate': 0.33,
                'location': 'Munich, Allemagne'
            },
            {
                'id': 'AFP_010',
                'title': 'Inflation zone euro - Baisse à 2.1% en octobre',
                'content': 'FRANCFORT - L\'inflation dans la zone euro continue sa décrue et s\'établit à 2.1% en octobre, se rapprochant de l\'objectif de 2% de la BCE. Les marchés saluent cette évolution.',
                'category': 'économie',
                'publication_date': base_time - timedelta(hours=20, minutes=10),
                'last_update': base_time - timedelta(hours=19, minutes=35),
                'journalist': 'Isabelle Moreau',
                'sources': 'Eurostat, BCE',
                'keywords': ['inflation', 'zone euro', 'bce', 'économie', 'marchés'],
                'priority': 'NORMAL',
                'reliability_score': 0.98,
                'reach': 95000,
                'word_count': 298,
                'reading_time': 1,
                'engagement_rate': 0.24,
                'location': 'Francfort, Allemagne'
            }
        ]
        
        # Sauvegarder les données avec des dates fixes
        self._save_news_data(fixed_articles)
        return fixed_articles
    
    def _save_news_data(self, articles):
        """Sauvegarde les données avec dates converties en string"""
        data_to_save = []
        for article in articles:
            article_copy = article.copy()
            article_copy['publication_date'] = article_copy['publication_date'].isoformat()
            article_copy['last_update'] = article_copy['last_update'].isoformat()
            data_to_save.append(article_copy)
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    
    def get_news_sorted(self, sort_by='publication_date', ascending=False):
        """Retourne les news triées selon le critère choisi"""
        if sort_by == 'publication_date':
            return sorted(self.news_data, key=lambda x: x['publication_date'], reverse=not ascending)
        elif sort_by == 'priority':
            priority_order = {'URGENT': 0, 'FLASH': 1, 'NORMAL': 2}
            return sorted(self.news_data, key=lambda x: priority_order.get(x['priority'], 3))
        elif sort_by == 'category':
            return sorted(self.news_data, key=lambda x: x['category'])
        elif sort_by == 'engagement':
            return sorted(self.news_data, key=lambda x: x['engagement_rate'], reverse=True)
        elif sort_by == 'reach':
            return sorted(self.news_data, key=lambda x: x['reach'], reverse=True)
        else:
            return self.news_data
    
    def filter_news(self, categories=None, priorities=None, journalists=None, hours_back=24):
        """Filtre les news selon les critères spécifiés"""
        filtered_news = self.news_data.copy()
        
        # Filtre par période
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        filtered_news = [article for article in filtered_news if article['publication_date'] >= cutoff_time]
        
        # Filtre par catégories
        if categories:
            filtered_news = [article for article in filtered_news if article['category'] in categories]
        
        # Filtre par priorités
        if priorities:
            filtered_news = [article for article in filtered_news if article['priority'] in priorities]
        
        # Filtre par journalistes
        if journalists:
            filtered_news = [article for article in filtered_news if article['journalist'] in journalists]
        
        return filtered_news
    
    def get_summary_stats(self):
        """Retourne des statistiques sur les articles"""
        categories = {}
        priorities = {}
        journalists = {}
        
        for article in self.news_data:
            # Comptage par catégorie
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
            
            # Comptage par priorité
            prio = article['priority']
            priorities[prio] = priorities.get(prio, 0) + 1
            
            # Comptage par journaliste
            jour = article['journalist']
            journalists[jour] = journalists.get(jour, 0) + 1
        
        return {
            'total_articles': len(self.news_data),
            'categories': categories,
            'priorities': priorities,
            'journalists': journalists,
            'avg_engagement': np.mean([a['engagement_rate'] for a in self.news_data]),
            'total_reach': sum([a['reach'] for a in self.news_data]),
            'avg_reliability': np.mean([a['reliability_score'] for a in self.news_data])
        }

def main():
    """Interface principale du dashboard chronologique"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ AFP News Timeline - Chronologie Officielle</h1>
        <h3>📰 Liste chronologique avec dates fixes et tri avancé</h3>
        <p>🕐 Timestamps stables • 🔍 Tri multicritères • 📊 Statistiques temps réel</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation du gestionnaire de news
    if 'news_manager' not in st.session_state:
        st.session_state.news_manager = AFPNewsManager()
    
    news_manager = st.session_state.news_manager
    
    # Sidebar avec contrôles
    with st.sidebar:
        st.markdown("### ⚙️ Contrôles Chronologie")
        
        # Contrôles d'actualisation
        auto_refresh = st.checkbox("🔄 Actualisation automatique", value=False, 
                                  help="Active la mise à jour automatique (les dates restent fixes)")
        
        if auto_refresh:
            refresh_interval = st.slider("⏱️ Intervalle (secondes)", 1, 60, 10)
        
        if st.button("🔄 Actualiser maintenant", type="primary"):
            st.rerun()
        
        st.markdown("---")
        
        # Tri et filtres
        st.markdown("#### 📋 Tri et Filtres")
        
        sort_by = st.selectbox(
            "🔀 Trier par",
            options=['publication_date', 'priority', 'category', 'engagement', 'reach'],
            format_func=lambda x: {
                'publication_date': '🕐 Date de publication',
                'priority': '⚡ Priorité',
                'category': '📂 Catégorie',
                'engagement': '🔥 Engagement',
                'reach': '📊 Portée'
            }[x],
            help="Critère de tri des articles"
        )
        
        if sort_by == 'publication_date':
            ascending = st.radio("📅 Ordre chronologique", 
                               options=[False, True],
                               format_func=lambda x: "Plus récent en premier" if not x else "Plus ancien en premier")
        else:
            ascending = False
        
        # Filtres
        st.markdown("#### 🎛️ Filtres")
        
        all_categories = list(set([article['category'] for article in news_manager.news_data]))
        selected_categories = st.multiselect(
            "📂 Catégories",
            options=all_categories,
            default=all_categories,
            help="Sélectionnez les catégories à afficher"
        )
        
        selected_priorities = st.multiselect(
            "⚡ Priorités",
            options=['URGENT', 'FLASH', 'NORMAL'],
            default=['URGENT', 'FLASH', 'NORMAL'],
            help="Filtrez par niveau de priorité"
        )
        
        all_journalists = list(set([article['journalist'] for article in news_manager.news_data]))
        selected_journalists = st.multiselect(
            "👨‍💼 Journalistes",
            options=all_journalists,
            default=all_journalists,
            help="Filtrez par journaliste"
        )
        
        hours_back = st.slider(
            "⏰ Période (heures)",
            min_value=1,
            max_value=48,
            value=24,
            help="Nombre d'heures à remonter dans le temps"
        )
        
        st.markdown("---")
        
        # Options d'affichage
        st.markdown("#### 🖥️ Affichage")
        
        show_full_content = st.checkbox("📝 Afficher contenu complet", value=False)
        show_metadata = st.checkbox("📊 Afficher métadonnées", value=True)
        show_keywords = st.checkbox("🏷️ Afficher mots-clés", value=True)
        
        # Réinitialisation du cache
        if st.button("🗑️ Réinitialiser cache", type="secondary"):
            if news_manager.cache_file.exists():
                news_manager.cache_file.unlink()
            st.session_state.news_manager = AFPNewsManager()
            st.success("Cache réinitialisé ! Nouvelles dates générées.")
            st.rerun()
    
    # Filtrage et tri des news
    filtered_news = news_manager.filter_news(
        categories=selected_categories if selected_categories else None,
        priorities=selected_priorities if selected_priorities else None,
        journalists=selected_journalists if selected_journalists else None,
        hours_back=hours_back
    )
    
    # Tri selon le critère sélectionné
    if sort_by == 'publication_date':
        sorted_news = sorted(filtered_news, key=lambda x: x['publication_date'], reverse=not ascending)
    elif sort_by == 'priority':
        priority_order = {'URGENT': 0, 'FLASH': 1, 'NORMAL': 2}
        sorted_news = sorted(filtered_news, key=lambda x: priority_order.get(x['priority'], 3))
    elif sort_by == 'category':
        sorted_news = sorted(filtered_news, key=lambda x: x['category'])
    elif sort_by == 'engagement':
        sorted_news = sorted(filtered_news, key=lambda x: x['engagement_rate'], reverse=True)
    elif sort_by == 'reach':
        sorted_news = sorted(filtered_news, key=lambda x: x['reach'], reverse=True)
    
    # Statistiques globales
    stats = news_manager.get_summary_stats()
    
    st.markdown("### 📊 Statistiques Globales")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📰 Total Articles", stats['total_articles'], 
                 help="Nombre total d'articles AFP dans la base")
    
    with col2:
        st.metric("📈 Articles Filtrés", len(filtered_news), 
                 f"{len(filtered_news)/stats['total_articles']*100:.0f}% du total",
                 help="Nombre d'articles après filtrage")
    
    with col3:
        st.metric("🔥 Engagement Moyen", f"{stats['avg_engagement']:.1%}",
                 help="Taux d'engagement moyen sur toutes les plateformes")
    
    with col4:
        st.metric("📊 Portée Totale", f"{stats['total_reach']:,}",
                 help="Nombre total de personnes atteintes")
    
    with col5:
        st.metric("🎯 Fiabilité Moyenne", f"{stats['avg_reliability']:.1%}",
                 help="Score de fiabilité moyen des sources AFP")
    
    # Répartition par catégories
    st.markdown("### 📂 Répartition par Catégories")
    
    col_cat1, col_cat2 = st.columns(2)
    
    with col_cat1:
        # Graphique en secteurs des catégories
        fig_categories = px.pie(
            values=list(stats['categories'].values()),
            names=list(stats['categories'].keys()),
            title="Distribution des Articles par Catégorie",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with col_cat2:
        # Graphique en barres des priorités
        fig_priorities = px.bar(
            x=list(stats['priorities'].keys()),
            y=list(stats['priorities'].values()),
            title="Répartition par Niveau de Priorité",
            color=list(stats['priorities'].keys()),
            color_discrete_map={'URGENT': '#FF6B6B', 'FLASH': '#FFA502', 'NORMAL': '#70A1FF'}
        )
        fig_priorities.update_layout(showlegend=False)
        st.plotly_chart(fig_priorities, use_container_width=True)
    
    # Liste chronologique des articles
    st.markdown(f"### 🕐 Chronologie AFP - {len(sorted_news)} articles")
    st.markdown(f"**Tri actuel:** {sort_by.replace('_', ' ').title()} | **Période:** {hours_back}h")
    
    if not sorted_news:
        st.warning("Aucun article ne correspond aux critères de filtrage sélectionnés.")
    else:
        for i, article in enumerate(sorted_news):
            # Container pour chaque article
            with st.container():
                # Header de l'article avec priorité
                priority_class = f"priority-{article['priority'].lower()}"
                
                col_header1, col_header2, col_header3 = st.columns([3, 1, 1])
                
                with col_header1:
                    st.markdown(f"### {i+1}. {article['title']}")
                
                with col_header2:
                    st.markdown(f'<div class="{priority_class}">{article["priority"]}</div>', 
                               unsafe_allow_html=True)
                
                with col_header3:
                    st.markdown(f'<div class="category-tag">{article["category"].title()}</div>', 
                               unsafe_allow_html=True)
                
                # Informations principales
                col_info1, col_info2, col_info3 = st.columns([2, 1, 1])
                
                with col_info1:
                    if show_full_content:
                        st.markdown(f"**📝 Contenu:** {article['content']}")
                    else:
                        st.markdown(f"**📝 Résumé:** {article['content'][:150]}...")
                    
                    st.markdown(f"**👨‍💼 Journaliste:** {article['journalist']}")
                    st.markdown(f"**📍 Lieu:** {article['location']}")
                    st.markdown(f"**📚 Sources:** {article['sources']}")
                
                with col_info2:
                    # Timestamps fixes
                    pub_time = article['publication_date']
                    update_time = article['last_update']
                    
                    st.markdown('<div class="timestamp-fixed">📅 DATES FIXES</div>', 
                               unsafe_allow_html=True)
                    st.write(f"🕐 **Publié:** {pub_time.strftime('%d/%m/%Y %H:%M')}")
                    st.write(f"🔄 **MAJ:** {update_time.strftime('%d/%m/%Y %H:%M')}")
                    
                    # Fraîcheur
                    time_diff = datetime.now() - pub_time
                    hours_ago = time_diff.total_seconds() / 3600
                    
                    if hours_ago < 1:
                        freshness = "🟢 TRÈS FRAIS"
                    elif hours_ago < 6:
                        freshness = "🟡 RÉCENT"
                    elif hours_ago < 12:
                        freshness = "🔵 MODÉRÉ"
                    else:
                        freshness = "⚪ ANCIEN"
                    
                    st.markdown(f"**⏰ Fraîcheur:** {freshness}")
                    st.markdown(f"**📅 Il y a:** {hours_ago:.1f}h")
                
                with col_info3:
                    if show_metadata:
                        st.markdown("**📊 Métriques**")
                        st.write(f"📝 **Mots:** {article['word_count']}")
                        st.write(f"⏱️ **Lecture:** {article['reading_time']} min")
                        st.write(f"🎯 **Fiabilité:** {article['reliability_score']:.1%}")
                        st.write(f"📊 **Portée:** {article['reach']:,}")
                        st.write(f"🔥 **Engagement:** {article['engagement_rate']:.1%}")
                
                # Mots-clés
                if show_keywords:
                    st.markdown("**🏷️ Mots-clés:**")
                    keywords_html = ""
                    for keyword in article['keywords']:
                        keywords_html += f'<span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2px 8px; border-radius: 10px; margin: 2px; font-size: 0.8em; display: inline-block;">{keyword}</span> '
                    st.markdown(keywords_html, unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Footer avec informations système
    st.markdown("---")
    current_time = datetime.now()
    st.markdown(f"""
    <div style="text-align: center; color: #95A5A6; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px;">
        <p><strong>🔄 Dernière actualisation:</strong> {current_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>📊 Articles affichés:</strong> {len(sorted_news)}/{stats['total_articles']} | 
           <strong>⚙️ Mode:</strong> {"🟢 AUTO" if auto_refresh else "🔄 MANUEL"}</p>
        <p><strong>🗂️ Tri actuel:</strong> {sort_by.replace('_', ' ').title()} | 
           <strong>📂 Catégories:</strong> {len(selected_categories)} sélectionnées</p>
        <p><strong>✅ DATES FIXES:</strong> Les timestamps ne changent jamais lors des actualisations</p>
        <p><em>🏛️ AFP News Timeline - Chronologie Officielle avec Dates Stables</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Système d'actualisation automatique
    if auto_refresh:
        countdown_placeholder = st.empty()
        for i in range(refresh_interval, 0, -1):
            countdown_placeholder.info(f"🔄 Prochaine actualisation dans {i} secondes... (Dates fixes conservées)")
            time.sleep(1)
        countdown_placeholder.empty()
        st.rerun()

if __name__ == "__main__":
    main()