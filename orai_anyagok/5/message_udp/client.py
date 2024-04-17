import sys
import socket

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = b"Hello server"
print("Üzenet:", msg.decode())
sock.sendto(msg, (server_addr, server_port))
answer, _ = sock.recvfrom(1024)
print("Kapott válasz:", answer.decode())
sock.close()