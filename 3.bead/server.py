import random
import select
import socket
import struct
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
format = "1s i"
packer = struct.Struct(format)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))

sock.listen(5)

inputs = [sock]

value = random.randint(1, 100)
guessed = False


def calculate(op, guess):
    global guessed
    if guessed:
        return b"V"

    if op == b"<":
        return b"I" if value < guess else b"N"
    elif op == b">":
        return b"I" if value > guess else b"N"
    elif op == b"=":
        guessed = value == guess
        return b"Y" if guessed else b"K"


while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                inputs.append(connection)
            else:
                msg = s.recv(packer.size)

                if not msg:
                    s.close()
                    inputs.remove(s)
                    continue

                parsed = packer.unpack(msg)
                result = calculate(*parsed)
                msg = packer.pack(result, 0)
                s.sendall(msg)

        # if len(inputs) == 1:
        #     value = random.randint(1, 100)
        #     guessed = False

    except Exception as e:
        for s in inputs:
            s.close()
        break
