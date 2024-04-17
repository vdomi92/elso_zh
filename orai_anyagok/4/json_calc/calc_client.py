import sys
import socket
import random
import struct
import json

server_addr = sys.argv[1]
server_port = int(sys.argv[2])
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((server_addr, server_port))

ops = ["+", "-", "*", "/"]

packer = struct.Struct("i i c")
# print(struct.calcsize('i i c'))
# vagy
# print(packer.size)

oper1 = random.randint(1, 100)
oper2 = random.randint(1, 100)
op = random.choice(ops)

json_request = {"oper1" : oper1, "oper2" : oper2, "op":op}

#msg = packer.pack(oper1, oper2, op.encode())
msg = json.dumps(json_request).encode()
print("Üzenet: {} {} {}".format(oper1, op, oper2))
sock.sendall(msg)

msg = sock.recv(BUFFER_SIZE)
#parsed_msg = packer.unpack(msg)
parsed_msg = json.loads(msg.decode())
print("Kapott eredmény: {}".format(parsed_msg["result"]))

sock.close()