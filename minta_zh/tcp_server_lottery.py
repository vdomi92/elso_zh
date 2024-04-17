import socket
import select
import random
import struct

BUFFER_SIZE = 1024
WINNING_NUM_COUNT = 5
WINNING_NUM_LOWEST = 1
WINNING_NUM_HIGHEST = 20

def genWinNumbers():
    numbers = []
    while len(numbers) < WINNING_NUM_COUNT:
        next = str(random.randint(WINNING_NUM_LOWEST,WINNING_NUM_HIGHEST))
        if next not in numbers:    
            numbers.append(next)# itt is encode/decode() string formátuma miatt string kell
    return numbers

def getMatchingCount(client_guess, winning_numbers):
    count = 0
    for i in range(WINNING_NUM_COUNT):
        if client_guess[i] in winning_numbers:
            count += 1
    return count

## msg_string example: 1:3:4:10:20:243  ...:243 = feltett pénz
def getClientGuess(msg_string):
    guessed_numbers = msg_string.split(":")
    amount = guessed_numbers[WINNING_NUM_COUNT]
    del guessed_numbers[-1]
    return (amount,guessed_numbers)

def strToInt(str_list):
    result = []
    for i in range(len(str_list)):
        result.append(int(str_list[i]))
    return result

server_addr = 'localhost'
server_port = 10006

history_server_addr = 'localhost'
history_server_port = 10007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ne kérdezd mért kell ez a sor
sock.bind((server_addr, server_port))

history_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#history_sock.bind((history_server_addr, history_server_port))

sock.listen(5)

inputs = [sock]
timeout = 1.0

# kihúzott szám, játékosok tippje, nyereményük
packer = struct.Struct('11i')

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
                decoded_msg = msg.decode()
                print(f"The client's message: {decoded_msg}")
                
                winning_numbers = genWinNumbers()
                bet_amount, client_guess = getClientGuess(decoded_msg)
                matching_guesses_count = getMatchingCount(client_guess, winning_numbers)
                amount_won = (int(bet_amount) * matching_guesses_count)

                response = f"Winning numbers were: {winning_numbers}. You have guessed {matching_guesses_count} correctly. Reward is {amount_won}."
                s.sendall(response.encode())
                print(f"SENT RESPONSE: Winning numbers were: {winning_numbers}. You have guessed {matching_guesses_count} correctly. Reward is {amount_won}.")

                # history server üzenet
                winning_numbers = strToInt(winning_numbers)
                guessed_numbers = strToInt(client_guess)
                print(f"Trying to pack:")
                print(f"Winning numbers: {winning_numbers}")
                print(f"Guessed numbers: {guessed_numbers}")
                print(f"Amount won: {amount_won}")
                packed_msg = packer.pack(*winning_numbers, *guessed_numbers, amount_won)
                history_sock.sendto(packed_msg, (history_server_addr, history_server_port))

    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        history_sock.close()
        print("Server closing")
        break