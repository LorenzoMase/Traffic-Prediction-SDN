import socket
import time
import random
import threading

parole_conversazione = [
    "ciao", "come", "stai", "bene", "grazie", "tu", "oggi", "domani", "ieri", "andiamo",
    "dove", "perché", "ok", "sì", "no", "forse", "va", "bene", "tempo", "scuola",
    "lavoro", "casa", "amici", "famiglia", "cibo", "bere", "film", "musica", "libri", "studio",
    "viaggio", "macchina", "treno", "soldi", "problema", "idea", "domanda", "risposta", "paese", "città",
    "mare", "montagna", "festa", "notte", "giorno", "settimana", "mese", "anno", "voglio", "posso"
]
# Server address
server_address = ("10.0.0.5", 65000)

# Receiving message function
def ricevi_messaggi(client_socket):
    """Funzione per ricevere messaggi dal server."""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Connessione chiusa dal server.")
                break
            print(f"{data.decode('utf-8')}")
        except ConnectionResetError:
            print("Connessione chiusa dal server.")
            break


# Connection with client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print("Connessione al server...")
    client_socket.connect(server_address)
    print("Connesso!")
    
    identificazione = "IDENTIFY h2"
    client_socket.sendall(identificazione.encode("utf-8"))
    print(f"Inviato al server: {identificazione}")

    # Thread to receive and send at the same time
    thread_ricezione = threading.Thread(target=ricevi_messaggi, args=(client_socket,))
    thread_ricezione.daemon = True
    thread_ricezione.start()
    time.sleep(20)

    for _ in range(10000):
        parola = random.choice(parole_conversazione)
        client_socket.sendall(parola.encode("utf-8"))
        print(f"Inviato: {parola}")

    print("Comunicazione terminata. In attesa di eventuali messaggi dal server...")
    time.sleep(10)
