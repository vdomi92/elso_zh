import sys
import socket
import struct
import select

proxy_addr = sys.argv[1]
proxy_port = int(sys.argv[2])
server_addr = sys.argv[3]
server_port = int(sys.argv[4])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((proxy_addr, proxy_port))

sock.listen(5)

proxySock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


packer = struct.Struct("i i c")

inputs = [sock]

while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Someone has connected: {client_info[0]}:{client_info[1]}")
                inputs.append(connection)
            else:
                msg = s.recv(packer.size)
                if not msg:
                    s.close()
                    print("The client has terminated the connection")
                    inputs.remove(s)
                    continue
                parsed_msg = packer.unpack(msg)
                print(
                    f"The client's message: {parsed_msg[0]} {parsed_msg[2].decode()} {parsed_msg[1]}"
                )
                #msg = packer.pack(parsed_msg[0], parsed_msg[1], parsed_msg[2])
                proxySock.sendto(msg, (server_addr, server_port))
                result, _ = proxySock.recvfrom(packer.size)
                parsed_msg = packer.unpack(result)
                print(
                    f"The server's response: {parsed_msg[0]} {parsed_msg[2].decode()} {parsed_msg[1]}"
                )
                s.sendall(result)

    except KeyboardInterrupt:
        print("Proxy shutting down")
        proxySock.close()
        sock.close()
        break