import sys
import socket
import random
import struct
import time

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

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

msg = packer.pack(oper1, oper2, op.encode())
print("Ăzenet: {} {} {}".format(oper1, op, oper2))
sock.sendall(msg)

msg = sock.recv(packer.size)
parsed_msg = packer.unpack(msg)
print("Kapott eredmĂŠny: {}".format(parsed_msg[0]))

sock.close()