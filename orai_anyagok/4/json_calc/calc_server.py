import sys
import socket
import struct
import json

server_addr = sys.argv[1]
server_port = int(sys.argv[2])
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((server_addr, server_port))

sock.listen(5)

ops = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: int(x / y),
}

packer = struct.Struct("i i 1s")  # = Struct('2i s')
conn, addr = sock.accept()
print("Valaki csatlakozott:", addr)
while True:
    msg = conn.recv(BUFFER_SIZE)
    if not msg:
        print("A kliens lezárta a kapcsolatot")
        break
    #parsed_msg = packer.unpack(msg)
    parsed_msg = json.loads(msg.decode())
    print(
        "A kliens üzenete: {} {} {}".format(
            parsed_msg["oper1"], parsed_msg["op"], parsed_msg["oper2"]
        )
    )
    result = ops[parsed_msg["op"]](parsed_msg["oper1"], parsed_msg["oper2"])
    json_result = {"result" : result}
    
    #msg = packer.pack(result, 0, b"R")
    msg = json.dumps(json_result).encode()
    conn.sendall(msg)
    print("Elküldött válasz: {}".format(result))

conn.close()
sock.close()