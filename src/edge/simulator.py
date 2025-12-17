import numpy as np
import time
from datetime import datetime
import requests

class MachineSimulator:
    """Simulateur d'une machine industrielle d'une usine Automobile."""
    
    def __init__(self, machine_id="RENAULT_MBG_L1"):
        self.machine_id = machine_id

    def generate_data(self):
        """Produit une lecture de capteur réaliste."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Comportement normal (Baseline)
        vibration = np.random.normal(10, 0.5)
        temperature = np.random.normal(65, 1.2)
        
        # Simulation d'une anomalie aléatoire (environ 5% du temps)
        # Très important pour tester ton futur modèle d'IA
        is_anomaly = 0
        if np.random.random() > 0.95:
            vibration += np.random.uniform(7, 12)  # Pic de vibration
            temperature += np.random.uniform(15, 25) # Surchauffe
            is_anomaly = 1

        return {
            "timestamp": timestamp,
            "machine_id": self.machine_id,
            "vibration": round(vibration, 2),
            "temperature": round(temperature, 2),
            "anomaly_flag": is_anomaly
        }

if __name__ == "__main__":
    sim = MachineSimulator()
    API_URL = "http://127.0.0.1:8000/ingest"
    
    print("🚀 Connexion au système MES et démarrage du simulateur...")
    
    try:
        while True:
            data = sim.generate_data()
            try:
                # Envoi de la donnée par une requête HTTP POST
                response = requests.post(API_URL, json=data)
                if response.status_code == 200:
                    print(f"✅ Transmis au MES : Vib={data['vibration']} | Temp={data['temperature']}")
                else:
                    print(f"⚠️ Problème de transmission : {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur de connexion au serveur API : {e}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 Simulation arrêtée.")