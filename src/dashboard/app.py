import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

st.set_page_config(page_title="Ampere Smart Factory", layout="wide")

st.title("🚗 Automobile ElectriCity - Monitoring Temps Réel")

# Fonction pour lire les logs générés par l'API
def get_data():
    if os.path.exists("data/factory_logs.csv"):
        df = pd.read_csv("data/factory_logs.csv")
        return df.tail(30) # On affiche les 30 derniers points
    return pd.DataFrame()

# Mise à jour automatique de l'interface
placeholder = st.empty()

while True:
    df = get_data()
    with placeholder.container():
        if not df.empty:
            # Indicateurs de performance (KPIs)
            m1, m2, m3 = st.columns(3)
            m1.metric("Vibration Actuelle", f"{df['vibration'].iloc[-1]} Hz")
            m2.metric("Température", f"{df['temperature'].iloc[-1]} °C")
            
            last_status = df['anomaly_flag'].iloc[-1]
            if last_status == 1:
                st.error("🚨 ALERTE : Comportement anormal détecté par l'IA !")
            else:
                st.success("✅ État de la ligne : NOMINAL")

            # Graphique interactif
            fig = px.line(df, x='timestamp', y=['vibration', 'temperature'], title="Flux IoT en direct")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("En attente de données du système MES...")
    
    time.sleep(2)