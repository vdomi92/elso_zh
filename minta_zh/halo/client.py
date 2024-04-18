import socket

BUFFER_SIZE = 1024
server_addr = 'localhost'
server_port = 10006

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((server_addr, server_port))

sock.sendall("Kerek feladatot".encode())
print("sent: kerem a feladatot")
while True:
    rec_msg = sock.recv(BUFFER_SIZE)
    if not rec_msg:
        continue

    print(f"Recieved msg: {rec_msg.decode()}")

    if rec_msg.decode() == "Meg nincs":
        rec_msg = sock.recv(BUFFER_SIZE)

    if rec_msg.decode() == "Tessek a feladat":
        sock.sendall("Koszonjuk".encode())
        print("sent: Köszönjük")
