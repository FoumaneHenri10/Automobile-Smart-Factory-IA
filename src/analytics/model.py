import pandas as pd
from sklearn.ensemble import IsolationForest 
import joblib # Pour sauvegarder le modèle
import os

class AnomalyDetector:
    def __init__(self):
        # On définit le modèle : contamination=0.05 signifie qu'on attend environ 5% d'anomalies
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.data_path = "data/factory_logs.csv"

    def train(self):
        """Entraîne le modèle sur les données collectées."""
        if not os.path.exists(self.data_path):
            print("❌ Erreur : Le fichier de données n'existe pas encore.")
            return
        
        df = pd.read_csv(self.data_path)
        
        # On utilise uniquement les colonnes numériques pour l'entraînement
        X = df[['vibration', 'temperature']]
        
        print(f"🧠 Entraînement du modèle sur {len(df)} relevés...")
        self.model.fit(X)
        
        # Sauvegarde du modèle pour l'utiliser en temps réel plus tard
        joblib.dump(self.model, "src/analytics/trained_model.pkl")
        print("✅ Modèle sauvegardé sous 'src/analytics/trained_model.pkl'")

    def predict_live(self, vibration, temperature):
        """Prédit si un nouveau relevé est une anomalie."""
        model = joblib.load("src/analytics/trained_model.pkl")
        prediction = model.predict([[vibration, temperature]])
        # Isolation Forest renvoie -1 pour une anomalie et 1 pour une donnée normale
        return "⚠️ ANOMALIE" if prediction[0] == -1 else "✅ NORMAL"

if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.train()