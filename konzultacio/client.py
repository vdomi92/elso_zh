import sys
import socket
import random
import struct
import json
import time

server_addr = "localhost"
server_port = 10002
history_addr = "localhost"
history_port = 10003
BUFFER_SIZE = 1024

credentials_to_try = sys.argv[1:]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.connect((server_addr, server_port))

for i in range(0, len(credentials_to_try), 2):
    credentials = {
        "username": credentials_to_try[i],
        "password": credentials_to_try[i + 1],
    }
    msg = json.dumps(credentials).encode()
    print(f"Message: {credentials}")
    sock.sendall(msg)

    msg = sock.recv(BUFFER_SIZE)
    print(f"Received result: {msg.decode()}")
    credentials["result"] = msg.decode()
    request = json.dumps(credentials).encode()
    udp_sock.sendto(request, (history_addr, history_port))
    answer, _ = udp_sock.recvfrom(1024)
    time.sleep(1)

sock.close()
