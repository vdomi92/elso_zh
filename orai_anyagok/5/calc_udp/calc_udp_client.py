import sys
import socket
import random
import struct
import time

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ops = ['+', '-', '*', '/']

packer = struct.Struct('i i c')

for nrnd in range(10):
	oper1 = random.randint(1,100)
	oper2 = random.randint(1,100)
	op = ops[nrnd % len(ops)]

	msg = packer.pack(oper1, oper2, op.encode())
	print( "Ăzenet: {} {} {}".format(oper1, op, oper2))	
	sock.sendto( msg,(server_addr, server_port))
	msg, _ = sock.recvfrom(packer.size)
	parsed_msg = packer.unpack( msg )
	print( "Kapott eredmĂŠny: {}".format(parsed_msg[0]))
	time.sleep(2)
sock.close()

