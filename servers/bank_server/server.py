#! /usr/bin/env python3


# Operations: SendTo, View, Deposit, Help
# SendTo [From] [To] [Amount]
# View [Username]
# Deposit [Username] [Amount]
# Help
import socket

# Creation of the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("10.0.0.4", 65000)
sock.bind(server_address)
sock.listen(1)
help_service=False
first_account = [1, "password", 10000, False]
second_account = [2, "password1", 20000, False]
third_account = [3, "password2", 30000, False]
login=False
print(f"Server avviato su {server_address[0]} porta {server_address[1]}")
while True:
    print("In attesa di connessioni...")
    connection, client_address = sock.accept()
    print(f"Connessione stabilita con {client_address}")
    # Someone connecting
    try:
        connection.sendall(b"Welcome to YourBank.com!\nCommand q to quit!\n")
        while True:
            # Authentication
            if login==False:
                connection.sendall(b"Insert username or insert q to quit: ")
                data = connection.recv(1024)
            if login==False:
                username=data.decode('utf-8')
                username=int(username)
                print(username)
                if username==first_account[0]:
                    connection.sendall(b"Insert password: ")
                    data = connection.recv(1024)
                    password=data.decode('utf-8').strip().split()
                    if password[0]==first_account[1]:
                        first_account[3]=True
                        login=True
                    else:
                        connection.sendall(b"Wrong password")
                        connection.close()
                elif username==second_account[0]:
                    connection.sendall(b"Insert password: ")
                    data = connection.recv(1024)
                    password=data.decode('utf-8').strip().split()
                    if password[0]==second_account[1] :
                        second_account[3]=True
                        login=True
                    else:
                        connection.sendall(b"Wrong password")
                        connection.close()
                elif username==third_account[0]:
                    connection.sendall(b"Insert password: ")
                    data = connection.recv(1024)
                    password=data.decode('utf-8').strip().split()
                    if password[0]==third_account[1]:
                        third_account[3]=True
                        login=True
                    else:
                        connection.sendall(b"Wrong password")
                        connection.close()
                elif username=="q":
                    connection.close()
                else:
                    connection.sendall(b"Invalid input")
                    break
            # Waiting for operations after authentication
            connection.sendall(b"Type an operation: ")
            data = connection.recv(1024)
            if data:
                # Split and decoding of the input
                input_data = data.decode('utf-8').strip()
                try:
                    op=""
                    username=0
                    amount=0
                    fusername=0
                    tusername=0
                    arguments_check = input_data.split()
                    arguments_count=len(arguments_check)
                    if arguments_count==2:
                        op, username=arguments_check
                        username=int(username)
                    elif arguments_count==3:
                        op, username, amount=arguments_check
                        username=int(username)
                        amount=float(amount)
                    elif arguments_count==4:
                        op, fusername, tusername, amount=arguments_check
                        fusername=int(fusername)
                        tusername=int(tusername)
                        amount=float(amount)
                    # Help command definition
                    elif arguments_count==1 and arguments_check[0]=="Help" and login==True:
                        help_service=True
                        connection.sendall(f"Usage:\n\tView [Username]\n\t Deposit [Username] [Amount]\n\t SendTo [From_username] [To_username] [Amount]\nUsernames: 1, 2, 3\n".encode('utf-8'))
                    elif arguments_count==1 and arguments_check[0]=="q":
                        connection.close()
                    else:
                        connection.sendall(b"Invalid Input")
                    # SendTo function
                    if op == "SendTo":
                        # SendTo if fusername==1
                        if fusername == 1 and first_account[3]==True:
                            if first_account[2] - amount < 0:
                                connection.sendall(b"Error: Missing funds. To deposit, use the Deposit service\n")
                            else:
                                first_account[2] -= amount
                            if tusername == 1:
                                connection.sendall(b"Error: Invalid input. To deposit, use the Deposit service\n")
                            elif tusername == 2:
                                second_account[2] += amount
                            elif tusername == 3:
                                third_account[2] += amount
                            connection.sendall(f"Operation completed, your current balance: {first_account[2]}\n".encode('utf-8'))
                        # SendTo if fusername == 2
                        elif fusername == 2 and second_account[3]==True:
                            if second_account[2] - amount < 0:
                                connection.sendall(b"Error: Missing funds. To deposit, use the Deposit service\n")
                            else:
                                second_account[2]-=amount
                            if tusername==1:
                                first_account[2]+=amount
                            elif tusername==2:
                                connection.sendall(b"Error: Invalid input. To deposit, use the Deposit service\n")
                            elif tusername==3:
                                third_account[2]+= amount
                            connection.sendall(f"Operation completed, your current balance: {second_account[2]}\n".encode('utf-8'))
                        # SendTo if fusername == 3
                        elif fusername==3 and third_account[3]==True:
                            if third_account[2]-amount < 0:
                                connection.sendall(b"Error: Missing funds. To deposit, use the Deposit service\n")
                                break
                            else:
                                third_account[2]-=amount
                            if tusername==1:
                                first_account[2]+=amount
                            elif tusername == 2:
                                second_account[2]+=amount
                            elif tusername==3:
                                connection.sendall(b"Error: Invalid input. To deposit, use the Deposit service\n")
                                break
                            connection.sendall(f"Operation completed, your current balance: {third_account[2]}\n".encode('utf-8'))
                        else:
                            connection.sendall(b"Permission Denied\n")
                    # View function
                    elif op == "View":
                        if username==1 and first_account[3]==True:
                            connection.sendall(f"Your balance is: {first_account[2]}\n".encode('utf-8'))
                        elif username==2 and second_account[3]==True:
                            connection.sendall(f"Your balance is: {second_account[2]}\n".encode('utf-8'))
                        elif username==3 and third_account[3]==True:
                            connection.sendall(f"Your balance is: {third_account[2]}\n".encode('utf-8'))
                        else:
                            connection.sendall(b"Permission Denied\n")
                    # Deposit function
                    elif op == "Deposit":
                        if username==1 and first_account[3]==True:
                            first_account[2]+=amount
                            connection.sendall(f"Operation completed, your current balance: {first_account[2]}\n".encode('utf-8'))
                        elif username==2 and second_account[3]==True:
                            second_account[2]+=amount
                            connection.sendall(f"Operation completed, your current balance: {second_account[2]}\n".encode('utf-8'))
                        elif username==3 and third_account[3]==True:
                            third_account[2]+=amount
                            connection.sendall(f"Operation completed, your current balance: {third_account[2]}\n".encode('utf-8'))
                        else:
                            connection.sendall(b"Permission Denied\n")
                    elif help_service==False:
                        connection.sendall(b"Error: Invalid input. Function: Help, View, Deposit, SendTo\n")
                except ValueError:
                    connection.sendall(b"Errore: Invalid input. How to use: Help\n")
            else:
                print("No data, closing connection.")
    finally:
        connection.close()
