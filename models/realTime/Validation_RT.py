import scapy.all as scapy
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

model = joblib.load('model.pkl')

pcap_file = 'validation.pcap'

# Funzioni per preprocessare i pacchetti
def process_packet(packet):
    try:
        src_ip = packet[scapy.IP].src if scapy.IP in packet else None
        dst_ip = packet[scapy.IP].dst if scapy.IP in packet else None
        protocol = packet[scapy.IP].proto if scapy.IP in packet else None
        
        return {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol
        }
    except Exception as e:
        print(f"Errore nel processare il pacchetto: {e}")
        return None

def process_length(packet):
    try:
        length = len(packet) if packet else 0
        
        return {
            "length": length,
        }
    except Exception as e:
        print(f"Errore nel processare il pacchetto: {e}")
        return None
packets = scapy.rdpcap(pcap_file)

data = []
labels = []

for packet in packets:
    processed_data = process_packet(packet)
    processed_length = process_length(packet)
    if processed_data:
        data.append(processed_data)
        labels.append(processed_length["length"]) 

df = pd.DataFrame(data)

# Pre-elaborazione dei dati (one-hot encoding)
X = pd.get_dummies(df, columns=["src_ip", "dst_ip", "protocol"], dummy_na=True).fillna(0)
X.to_csv('X.csv', index=False)
# Previsioni sulla lunghezza dei pacchetti
predictions = model.predict(X)
mse = mean_squared_error(labels, predictions)
mae = mean_absolute_error(labels, predictions)
r2 = r2_score(labels, predictions)

print(f"Errore Quadratico Medio (MSE): {mse}")
print(f"Errore Assoluto Medio (MAE): {mae}")
print(f"Coefficiente di Determinazione (R^2): {r2}")

# Salvataggio dei risultati in un file CSV
predictions_df = pd.DataFrame({
    'Packet Index': range(1, len(predictions) + 1),
    'Real Length': labels,
    'Predicted Length': predictions
})
predictions_df.to_csv('predictions.csv', index=False)

print("Le previsioni sono state salvate in 'predictions.csv'")
