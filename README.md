# 🚗 Automobile Smart Factory IA : Maintenance Prédictive & IoT

Ce projet simule une architecture **Industrie 4.0** complète, conçue pour l'optimisation des processus de production et la maintenance prédictive au sein d'une usine Automobile Electric.

L'objectif est de détecter en temps réel des anomalies sur une ligne de production (vibrations, surchauffes) grâce à une approche **End-to-End** : de l'automate (Edge) au Dashboard (Digital Twin), en passant par une IA d'analyse.

## 🌟 Points Forts du Projet
- **Architecture Industrielle :** Simulation réaliste d'automates (Python POO).
- **Collecte Intelligente (MES) :** Développement d'une passerelle API robuste avec **FastAPI**.
- **IA & Maintenance Prédictive :** Détection d'anomalies via l'algorithme **Isolation Forest** (Scikit-Learn).
- **Digital Twin :** Dashboard de monitoring temps réel avec **Streamlit** et **Plotly**.

## 🏗️ Architecture du Système
1. **Edge Computing (`src/edge/`)** : Simulateur de capteurs IoT (Vibrations/Température) envoyant des données à haute fréquence.
2. **Data Gateway / MES (`src/api/`)** : API centrale réceptionnant les flux, archivant les données et déclenchant les diagnostics IA.
3. **Analytics Engine (`src/analytics/`)** : Modèle de Machine Learning entraîné pour distinguer le comportement normal des pannes imminentes.
4. **Supervision (`src/dashboard/`)** : Interface visuelle permettant aux opérateurs de visualiser l'état de la ligne.



## 🛠️ Technologies Utilisées
- **Langage :** Python 3.10+
- **Data & AI :** Pandas, Numpy, Scikit-Learn, Joblib
- **Communication :** FastAPI (REST API), Uvicorn, Requests
- **Visualisation :** Streamlit, Plotly

## 🚀 Installation et Utilisation

### 1. Prérequis
```bash
pip install -r requirements.txt
2. Lancement du Système (3 étapes)
Ouvrez trois terminaux distincts dans VS Code :

Terminal 1 - Le Cerveau (API + IA) :

Bash

python src/api/main.py

Terminal 2 - La Ligne de Production (Simulateur) :

Bash

python src/edge/simulator.py

Terminal 3 - La Supervision (Dashboard) :

Bash

streamlit run src/dashboard/app.py

📊 Impact pour une entreprise Automobile
Ce projet répond aux enjeux d'une Usine 4.0 en permettant :

Une réduction des arrêts de production non planifiés grâce à la maintenance prédictive.

Une digitalisation complète des flux de données machines (IoT/MES).

Une aide à la décision pour les équipes de maintenance grâce au diagnostic IA instantané.