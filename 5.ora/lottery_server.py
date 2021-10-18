import socket
import select
import struct
import random
import json

TCP_IP = 'localhost'
TCP_PORT = 10000
BUFFER_SIZE = 1024
history_packer = struct.Struct(" ".join(["i"]*11))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))

history_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
history_addr = ("localhost", 10001)

sock.listen(5)

inputs = [sock]

nums = random.sample(range(1, 21), 5)

def calculate_winnings(bet):
    return bet["amount"] * len(set(nums) & set(bet["nums"]))

while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Csatlakozott {client_info}")
                inputs.append(connection)
            else:
                msg = s.recv(BUFFER_SIZE)

                if not msg:
                    s.close()
                    print("Valaki kilépett")
                    inputs.remove(s)
                    continue

                amount, *bet_nums = map(int, msg.split(":"))

                winnings = calculate_winnings({"amount": amount, "nums": bet_nums})
                answer = ":".join(map(str, [winnings, nums]))
                msg = answer.encode("UTF-8")

                s.sendall(msg)

                print(f"Elküldött válasz: {answer}")

                msg = history_packer.pack(*nums, *bet_nums, winnings)
                history_sock.sendto(msg, history_addr)
                
    except Exception as e:
        for s in inputs:
            s.close()
        print("Server closing")
        raise e
        break
