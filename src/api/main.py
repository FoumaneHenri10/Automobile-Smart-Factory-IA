from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
import joblib # Pour charger l'IA

app = FastAPI(title="Automobile ElectriCity - Intelligent MES")

# Modèle de données
class SensorData(BaseModel):
    timestamp: str
    machine_id: str
    vibration: float
    temperature: float
    anomaly_flag: int

# Chargement du modèle IA au démarrage de l'API
MODEL_PATH = "src/analytics/trained_model.pkl"

@app.post("/ingest")
async def ingest_data(data: SensorData):
    # 1. Sauvegarde classique
    file_path = "data/factory_logs.csv"
    df_save = pd.DataFrame([data.dict()])
    df_save.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
    
    # 2. Diagnostic par l'IA
    status = "Inconnu"
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        # Prédiction (Isolation Forest : 1 = Normal, -1 = Anomalie)
        prediction = model.predict([[data.vibration, data.temperature]])
        status = "✅ NORMAL" if prediction[0] == 1 else "⚠️ ALERTE : ANOMALIE DÉTECTÉE"
    
    print(f"📥 [{data.machine_id}] Diagnostic IA : {status}")
    
    return {
        "status": "success", 
        "ai_diagnostic": status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)