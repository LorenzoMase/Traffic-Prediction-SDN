import socket
import scapy.all as scapy
import threading
import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import joblib
import tempfile

data_lock = threading.Lock()
live_data = {"x": [], "y": []} 

def write_to_tempfile(temp_file, data):
    with open(temp_file, 'ab') as f:
        f.write(data)

# Funzione per processare src ip, dst ip, e protocol
def process_packet(packet):
    try:
        if packet.haslayer(scapy.IP):
            src_ip = packet[scapy.IP].src if scapy.IP in packet else None
            dst_ip = packet[scapy.IP].dst if scapy.IP in packet else None
            protocol = packet.proto
            print(f"src_ip: {src_ip}, dst_ip: {dst_ip}, protocol: {protocol}")
        return {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'protocol': protocol,
        }
    except Exception as e:
        print(f"Errore nell'elaborazione del pacchetto: {e}")
        return None

# Funzione per processare la length dei pacchetti
def process_length(packet):
    try:
        if packet.haslayer(scapy.IP):
            length = len(packet) if packet else None
            print(f"length: {length}")
        return {
            'length': length,
        }
    except Exception as e:
        print(f"Errore nell'elaborazione del pacchetto: {e}")
        return None

# Funzione per allenare il modello
def train_model_from_file(temp_file):
    print("Analisi dei pacchetti dal file temporaneo...")
    # Usa Scapy per leggere il file pcap
    packets = scapy.rdpcap(temp_file)

    data = []
    labels = []

    for packet in packets:
        processed_data = process_packet(packet)
        processed_length= process_length(packet)
        if processed_data and process_length is not None:
            labels.append(processed_length["length"])
            data.append(processed_data)
    print(f"Rilevati {len(data)} pacchetti.")
    if data:
        print("Inizio addestramento del modello...")
        df = pd.DataFrame(data)
        X = pd.get_dummies(df, columns=['src_ip', 'dst_ip', 'protocol'], dummy_na=True).fillna(0)
        y = np.array((labels)).astype(float)
        model = SGDRegressor()
        model.fit(X, y)
        print(f"Modello addestrato con {len(data)} campioni.")

        # Salva il modello aggiornato
        joblib.dump(model, "model.pkl")
        print("Modello salvato come 'model.pkl'")

# Inizializzazione del server in ascolto su tutte le interfacce
def start_tcp_server(host, port):
    print(f"Server TCP in ascolto su {host}:{port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        while True:
            print("In attesa di connessioni...")
            conn, addr = sock.accept()
            print(f"Connessione stabilita con {addr}")

            while True:
                raw_data = conn.recv(65535)
                if not raw_data:
                    break

                with data_lock:
                    live_data["x"].append(time.time()) 
                    live_data["y"].append(len(raw_data))
                write_to_tempfile(temp_file_path, raw_data)
                print(f"Ricevuti {len(raw_data)} byte")

            print("Connessione chiusa. Avvio dell'addestramento del modello...")
            train_model_from_file(temp_file_path)

            conn.close()

    except KeyboardInterrupt:
        print("\nInterruzione da tastiera, terminazione del server...")
    except Exception as e:
        print(f"Errore nel server: {e}")
    finally:
        sock.close()

def update_plot(frame):
    global live_data

    with data_lock:
        x = live_data["x"][-1000:]
        y = live_data["y"][-1000:]

    if len(x) == 0 or len(y) == 0:
        return

    if len(ax.lines) == 0:
        ax.plot(x, y, label="Pacchetti ricevuti", color="blue")
    else:
        ax.lines[0].set_xdata(x)
        ax.lines[0].set_ydata(y)

    ax.set_xlim(min(x) - 50, max(x) + 50)
    ax.set_ylim(min(y) - 300, max(y) + 10000)
    ax.set_title("Aggiornamento dati in arrivo in tempo reale")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Lunghezza dati (byte)")
    ax.legend()
    ax.grid(True)
    
# Definizione grafico
fig, ax = plt.subplots(figsize=(10, 6))

# Avvia il server in un thread separato
server_thread = threading.Thread(target=start_tcp_server, args=("0.0.0.0", 6343))
server_thread.daemon = True
server_thread.start()

# Avvia l'animazione con aggiornamento per ogni secondo
ani = FuncAnimation(fig, update_plot, interval=1000, blit=False)
plt.show()
