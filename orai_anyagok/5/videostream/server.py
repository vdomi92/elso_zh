#!/usr/bin/env python
# coding: utf-8

# source: https://github.com/jeremyfix/udp_video_streaming

# For debugging :
# - run the server and remember the IP of the server
# And interact with it through the command line:
# echo -n "get" > /dev/udp/192.168.0.39/1080
# echo -n "quit" > /dev/udp/192.168.0.39/1080

import socket
import sys
import sys
from videograbber import VideoGrabber

if(len(sys.argv) != 2):
		print("Usage : {} port".format(sys.argv[0]))
		print("e.g. {} 1080".format(sys.argv[0]))
		sys.exit(-1)

debug = True
jpeg_quality = 25
host = ""
port = int(sys.argv[1])

grabber = VideoGrabber(jpeg_quality)
grabber.start()
get_message = lambda: grabber.get_buffer()

running = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1.0)

# Bind the socket to the port
server_address = (host, port)

print('starting up on %s port %s\n' % server_address)

sock.bind(server_address)

while(running):
	try:
		try:
			data, address = sock.recvfrom(4)
			data = data.decode('utf-8')
			if(data == "get"):
					buffer = get_message()
					if buffer is None:
							continue
					if len(buffer) > 65507:
							print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
							sock.sendto("FAIL".encode('utf-8'),address)
							continue
					# We sent back the buffer to the client
					sock.sendto(buffer.tobytes(), address)
			elif(data == "quit"):
					grabber.stop()
					running = False
			elif(data == "clr"):
					grabber.ret()
		except socket.timeout:
			pass
	except KeyboardInterrupt:
		grabber.stop()
		running = False

print("Quitting..")
grabber.join()
sock.close()