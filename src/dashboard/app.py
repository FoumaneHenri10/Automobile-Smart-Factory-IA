import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

# DÉFINITION DES FONCTIONS
def log_intervention():
    new_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "site": "Hauts-de-France",
        "ligne": "MBG_L1",
        "statut": "Intervention effectuée"
    }
    df_log = pd.DataFrame([new_log])
    log_file = "data/interventions.csv"
    
    if not os.path.exists(log_file):
        df_log.to_csv(log_file, index=False)
    else:
        df_log.to_csv(log_file, mode='a', header=False, index=False)

def get_data():
    if os.path.exists("data/factory_logs.csv"):
        df = pd.read_csv("data/factory_logs.csv")
        return df.tail(50)
    return pd.DataFrame()

# Configuration de la page
st.set_page_config(
    page_title="Automobile Smart Factory AI - Dashboard",
    page_icon="🚗",
    layout="wide",
)

# Style CSS pour un look industriel
# Style CSS Avancé
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp {
        background-color: #f8f9fc;
    }
    
    /* Titre Principal Ultra Stylisé */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3rem !important;
        color: #1e293b;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding-bottom: 20px;
        border-bottom: 3px solid #FFB81C; /* Ligne jaune Renault */
        margin-bottom: 30px;
    }

    /* Cartes de Metrics (Plus lourdes et pro) */
    [data-testid="stMetricSimpleValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #00529B !important; /* Bleu profond */
    }
    
    .stMetric {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border-left: 8px solid #00529B !important; /* Barre d'accent */
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05) !important;
    }

    /* Style pour le conteneur IA et Action */
    .status-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # On charge l'image locale
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        # Repli sur un texte si l'image est manquante
        st.title("🚗 Automobile AI")
        
    st.title("Contrôle Usine")
    st.info("📍 Site : Hauts-de-France\n\n🏭 Ligne : MBG_L1")
    st.markdown("---")
    if st.button("🔄 Actualiser Manuellement", key="refresh_sidebar"):
        st.rerun()

# --- HEADER ---
# Titre avec classe CSS personnalisée
st.markdown('<h1 class="main-title">🚗 Automobile Smart Factory AI</h1>', unsafe_allow_html=True)
st.subheader("Monitoring Temps Réel - Pôle Industriel")
st.caption(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")

# Fonction pour charger les données
def get_data():
    if os.path.exists("data/factory_logs.csv"):
        df = pd.read_csv("data/factory_logs.csv")
        return df.tail(50)
    return pd.DataFrame()

# --- AFFICHAGE ---
df = get_data()

if not df.empty:
    # 1. KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    last_vib = df['vibration'].iloc[-1]
    last_temp = df['temperature'].iloc[-1]
    last_anomaly = df['anomaly_flag'].iloc[-1]
    
    col1.metric("Vibration (Hz)", f"{last_vib}", f"{round(last_vib - 10, 2)} vs nom.")
    col2.metric("Température (°C)", f"{last_temp}", f"{round(last_temp - 65, 2)} vs nom.")
    
    with col3:
        st.write("**Diagnostic IA**")
        if last_anomaly == 1:
            st.error("⚠️ ANOMALIE")
        else:
            st.success("✅ NOMINAL")
            
    with col4:
        st.write("**Action**")
        if st.button("📦 Log Intervention", key="btn_intervention"):
            log_intervention() # On appelle la fonction
            st.toast("✅ Rapport envoyé au service Maintenance", icon="🛠️")
            st.balloons() # Optionnel : petit effet visuel pour la vidéo !

    st.markdown("---")

    # 2. Graphiques
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Flux de données capteurs")
        fig = px.line(df, x='timestamp', y=['vibration', 'temperature'],
                     color_discrete_map={"vibration": "#00529B", "temperature": "#FFB81C"},
                     template="plotly_white")
        # Correction width='stretch' pour la nouvelle version de Streamlit
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.subheader("Historique récent")
        st.dataframe(df[['timestamp', 'vibration', 'temperature', 'anomaly_flag']].tail(10), 
                     hide_index=True, width='stretch')

    # --- AUTO-REFRESH (Toutes les 2 secondes) ---
    time.sleep(2)
    st.rerun()

else:
    st.warning("⚠️ En attente de flux provenant du système MES... Lancez le simulateur.")
    time.sleep(2)
    st.rerun()