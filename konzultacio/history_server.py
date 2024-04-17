import sys
import socket
import json

server_addr = "localhost"
server_port = 10003

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_addr, server_port))

while True:
    try:
        data, client_addr = sock.recvfrom(1024)
        data = data.decode()
        print(client_addr, ":", data)
        interpreted_msg = json.loads(data)
        print(interpreted_msg)
        msg = b"OK"
        sock.sendto(msg, client_addr)
    except KeyboardInterrupt:
        break
sock.close()
print("Server terminated")
