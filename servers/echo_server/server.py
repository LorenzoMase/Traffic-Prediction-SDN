#! /usr/bin/env python3

import socket
import select

# Creation of the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("10.0.0.5", 65000)
sock.bind(server_address)
sock.listen(5)
print(f"Server avviato su {server_address[0]} porta {server_address[1]}")

# Dict to track connected clients
clients = {}

try:
    while True:
        readable, _, _ = select.select([sock] + list(clients.values()), [], [])
        
        for s in readable:
            if s is sock:
                # New connection
                connection, client_address = sock.accept()
                print(f"Connessione stabilita con {client_address}")
                connection.sendall(b"Benvenuto su MessChat! Identificati come 'h1' o 'h2': ")
                clients[client_address] = connection
            else:
                # Receiving traffic
                data = s.recv(1024)
                if data:
                    msg = data.decode('utf-8').strip()
                    if msg.startswith("IDENTIFY"):
                        # Identificazione del client
                        _, client_id = msg.split()
                        clients[client_id] = s
                        s.sendall(f"Identificato come {client_id}. Pronto a ricevere messaggi.\n".encode('utf-8'))
                    elif msg == "q":
                        # Closing the connection
                        print(f"Connessione chiusa con {client_address}")
                        del clients[client_address]
                        s.close()
                    else:
                        # Sending the messages received from h1 to h3 and the otherway around
                        sender = list(clients.keys())[list(clients.values()).index(s)]
                        if "10.0.0.1"== s.getpeername()[0]:
                            clients["h2"].sendall(f"Messaggio da h1: {msg}\n".encode('utf-8'))
                        elif "10.0.0.2"== s.getpeername()[0]:
                            clients["h1"].sendall(f"Messaggio da h2: {msg}\n".encode('utf-8'))
                        else:
                            s.sendall(b"Destinatario non disponibile.\n")
                else:
                    # Deleting clients disconnecting from the dict
                    print(f"Disconnessione di {client_address}")
                    s.close()
                    del clients[client_address]
except KeyboardInterrupt:
    print("\nServer interrotto manualmente. Chiusura...")
    sock.close()
