import sys
import socket
import struct
import select
import json
import hashlib


def check_credentials(stored_credentials, username, password):
    sha_object = hashlib.sha1()
    sha_object.update(password.encode())
    hash = sha_object.hexdigest()  # van sha_object.digest()
    if username in stored_credentials:
        if hash == stored_credentials[username]:
            return stored_credentials, "OK"
        else:
            return stored_credentials, "INCORRECT"
    else:
        stored_credentials[username] = hash
        return stored_credentials, "CREATED"


server_addr = "localhost"
creds_file = "creds.json"
server_port = 10002
BUFFER_SIZE = 1024


credentials = {}
with open(creds_file, "r") as f:
    credentials = json.load(f)

print(credentials)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((server_addr, server_port))

sock.listen(5)


inputs = [sock]
timeout = 1.0

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], timeout)

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                inputs.append(connection)
            else:
                msg = s.recv(BUFFER_SIZE)
                if not msg:
                    s.close()
                    print("The client has terminated the connection")
                    inputs.remove(s)
                    continue
                interpreted_msg = json.loads(msg.decode())
                print(f"The client's message: {interpreted_msg}")
                credentials, result = check_credentials(
                    credentials,
                    interpreted_msg["username"],
                    interpreted_msg["password"],
                )
                s.sendall(result.encode())
                print(f"Sent response: {result}")

    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        print("Server closing")
        break
