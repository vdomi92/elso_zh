import sys
import socket
import struct
import json

def appendResults(winning_nums, guessed_nums, amount_won, file_name):
    try:
        with open(file_name, 'r') as file:
            current_data = json.load(file)
    except (json.decoder.JSONDecodeError):
            current_data = []

    data_to_add = {
        'Winning numbers' : winning_nums,
        'Guessed numbers' : guessed_nums,
        'Amount won' : amount_won
        }
    current_data.append(data_to_add)
    with open(file_name, 'w') as file:
        json.dump(current_data, file)
    return

server_addr = 'localhost'
server_port = 10007
data_file_name = sys.argv[1] #filenevet megkell adni indításkor

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind( (server_addr, server_port) )

# kihúzott számok, játékosok tippje, nyereményük
packer = struct.Struct('11i')

while True:
    try:
        msg, _ = sock.recvfrom(packer.size)
        parsed_msg = packer.unpack(msg)
        print(f"PARSED_MSG: {parsed_msg}")
        print(
            f"The client's (lottery server) message:\n Winning numbers: {parsed_msg[0]}\n Client's guess: {parsed_msg[1]}\n Amount won: {parsed_msg[2]}"
        )
        winning_numbers = parsed_msg[:5]
        print(f"Parsed winning numbers: {winning_numbers}")
        guessed_numbers = parsed_msg[5:10]
        print(f"Parsed guessed numbers: {guessed_numbers}")
        amount_won = parsed_msg[10]
        print(f"Parsed amount won: {amount_won}")
        # kihúzott számok, játékosok tippje, nyereményük
        appendResults(winning_numbers, guessed_numbers, amount_won, data_file_name)

    except KeyboardInterrupt:
        print("History server shutting down")
        sock.close()
        break