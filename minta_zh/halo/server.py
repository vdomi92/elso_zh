import socket
import select
import sys

BUFFER_SIZE = 1024
server_addr = 'localhost'
server_port = 10006

clients_required = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ne kérdezd mért kell ez a sor
sock.bind((server_addr, server_port))

sock.listen(5)

inputs = [sock]
timeout = 1.0

connected_users = 0
clients = []

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], timeout)
        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                inputs.append(connection)
                connected_users += 1
                print(f"Connected users: {connected_users}")
            else:
                msg = s.recv(BUFFER_SIZE)
                if not msg:
                    continue

                print(f"The client's message: {msg}")
             
                if connected_users < clients_required:
                    s.sendall("Meg nincs".encode())
                    clients.append(s)
                else:
                    clients.append(s)

                if connected_users == clients_required:
                    i = 1
                    for client in clients:
                        print(f"Handling client: {i}")
                        i+=1
                        client.sendall("Tessek a feladat".encode())
                        print(f"sent: Tessek a feladat")
                        resp = client.recv(BUFFER_SIZE).decode()
                        print(f"recieved: {resp}")
                        client.sendall("Szivesen".encode())
                        continue
                    connected_clients = 0
                    clients = []
                
    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        print("Server closing")
        break