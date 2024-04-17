import socket
import random

BUFFER_SIZE = 1024
WINNING_NUM_COUNT = 5
WINNING_NUM_LOWEST = 1
WINNING_NUM_HIGHEST = 20

def guessNumbers():
    numbers = []
    while len(numbers) < WINNING_NUM_COUNT:
        next = str(random.randint(WINNING_NUM_LOWEST, WINNING_NUM_HIGHEST)) # string formátumban, mert a decode() stringet ad vissza
        if next not in numbers:
            numbers.append((next))
    return numbers

def createMessage(guessed_numbers, bet_amount):
    guessed_numbers.append(str(bet_amount)) # mindent is stringbe
    message = ':'.join(guessed_numbers)
    return message.encode() ## ebbűl lesz a bytes object

server_addr = 'localhost'
server_port = 10006

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((server_addr, server_port))

guessed_numbers = guessNumbers()
bet_amount = random.randint(1, 1000)
msg = createMessage(guessed_numbers, bet_amount)
print(f"Message is {msg.decode()} sent")
sock.sendall(msg)

rec_msg = sock.recv(BUFFER_SIZE)
print(f"Recieved message: {rec_msg.decode()}")

sock.close()