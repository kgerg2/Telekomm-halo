import socket
from struct import calcsize, pack, unpack
import sys
import random

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
a = random.randrange(10)
b = random.randrange(10)
op = random.choice([b"+", b"-", b"*", b"/"])
print(f"Kérés: {a} {op.decode()} {b}")
format = "i i 1s"
message = pack(format, a, b, op)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(message, (TCP_IP, TCP_PORT))
reply, _ = sock.recvfrom(calcsize("i"))

sock.close()

print("Válasz:", *unpack("i", reply))
