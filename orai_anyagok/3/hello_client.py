import socket
import sys

TCP_IP = "localhost"  #ekvivalens ezzel: "127.0.0.1"
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
message = b"hello server"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.sendall(message)
reply = sock.recv(BUFFER_SIZE)
sock.close()

print("VĂĄlasz:", reply.decode())