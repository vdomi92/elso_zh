import socket
for i in range(1,101):
    try:
        print(f"{i}:", socket.getservbyport(i, "tcp"))
    except OSError:
        print(f"{i}: Semmi")