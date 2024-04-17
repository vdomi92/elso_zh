import sys
import socket
import struct
import select
import time

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind( (server_addr, server_port) )

ops = { '+': lambda x,y: x+y, 
	'-': lambda x,y: x-y,
	'*': lambda x,y: x*y,
	'/': lambda x,y: int(x/y)}

packer = struct.Struct('i i c')

while True:
    data, client_addr = sock.recvfrom(packer.size)
    parsed_msg = packer.unpack(data)
    print("{} {} {}".format(parsed_msg[0], parsed_msg[2].decode(), parsed_msg[1]))
    result = ops[parsed_msg[2].decode()](parsed_msg[0], parsed_msg[1])
    msg = packer.pack(result,0,b"R")
    sock.sendto(msg,client_addr)
sock.close()