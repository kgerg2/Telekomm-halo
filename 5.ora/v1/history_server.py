import socket
import struct
import json
#import sys

TCP_IP = 'localhost'
TCP_PORT = 10001

history_location = "history.txt"

packer = struct.Struct(" ".join(["i"]*11))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((TCP_IP, TCP_PORT))


try:
    with open(history_location) as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

while True:
    try:
        data, claddr = sock.recvfrom(packer.size)
        msg = packer.unpack(data)
        nums = msg[:5]
        guesses = msg[5:10]
        winnings = msg[10]

        print(f"Új adat {claddr}-től: {nums=}, {guesses=}, {winnings=}")

        history.append({"nums": nums, "guesses": guesses, "winnings": winnings})

        with open(history_location, "w") as f:
            json.dump(history, f)

    except KeyboardInterrupt:
        break

sock.close()
