import telnetlib
from time import sleep

# Configuration of the server and operations file
host = "10.0.0.4"
port = 65000
input_file = "operations.txt"

try:
    # Connecting to the server
    telnet_connection = telnetlib.Telnet(host, port)
    print(f"Connesso a {host}:{port}")
    sleep(1)
    
    try:
        output = telnet_connection.read_very_eager().decode('utf-8')
        print("Dati ricevuti dal server inizialmente:")
        print(output)
    except EOFError:
        print("Nessun dato iniziale ricevuto dal server.")ù
        
    # Sending operations read from the output.txt fuile
    with open(input_file, "r") as infile:
        for line in infile:
            line = line.strip() 
            telnet_connection.write(line.encode('utf-8') + b'\n')
            print(f"Inviata: {line}")
            sleep(1)
            
            try:
                output = telnet_connection.read_very_eager().decode('utf-8')
                print("Dati ricevuti dal server:")
                print(output)
            except EOFError:
                print("Nessun dato ricevuto dopo l'invio.")

    # Closing the connection
    telnet_connection.close()
    print("Connessione chiusa.")

except Exception as e:
    print(f"Errore durante la connessione a {host}:{port}: {e}")
