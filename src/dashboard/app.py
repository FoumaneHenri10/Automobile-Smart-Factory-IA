import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Automobile Smart Factory AI - Dashboard",
    page_icon="🚗",
    layout="wide",
)

# Style CSS personnalisé pour un look "Industrie 4.0"
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b7/Renault_2021.svg", width=100)
    st.title("Contrôle Usine")
    st.info("📍 Site : Maubeuge\n\n🏭 Ligne : MBG_L1")
    st.markdown("---")
    st.write("📊 **Statut Système :**")
    st.success("API MES : Connectée")
    st.success("Modèle IA : Actif")

# --- HEADER ---
st.title("🚗 Ampere ElectriCity - Monitoring Temps Réel")
st.caption(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")

# Fonction pour charger les données
def get_data():
    if os.path.exists("data/factory_logs.csv"):
        df = pd.read_csv("data/factory_logs.csv")
        return df.tail(50)
    return pd.DataFrame()

# --- MAIN LAYOUT ---
placeholder = st.empty()

while True:
    df = get_data()
    
    with placeholder.container():
        if not df.empty:
            # 1. KPIs en haut
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
                st.write("**Maintenance**")
                st.button("📦 Log Intervention")

            st.markdown("---")

            # 2. Graphiques
            c1, c2 = st.columns([2, 1])
            
            with c1:
                st.subheader("Flux de données capteurs")
                fig = px.line(df, x='timestamp', y=['vibration', 'temperature'],
                             color_discrete_map={"vibration": "#00529B", "temperature": "#FFB81C"},
                             template="plotly_white")
                fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.subheader("Historique récent")
                # Affichage des 10 dernières lignes avec style
                st.dataframe(df[['timestamp', 'vibration', 'temperature', 'anomaly_flag']].tail(10), 
                             hide_index=True, use_container_width=True)

        else:
            st.warning("⚠️ En attente de flux provenant du système MES... Lancez le simulateur.")
            
    time.sleep(2)