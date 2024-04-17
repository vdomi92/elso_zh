import socket
import sys

TCP_IP = 'localhost' # "127.0.0.1"
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024
reply = b'Hello kliens'     #reply.encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

conn, addr = sock.accept()
print('Valaki csatlakozott:', addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
            break
    print("Üzenet:", data.decode())
    conn.sendall(reply)
conn.close()
sock.close()