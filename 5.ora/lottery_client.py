import sys
import socket
import random
import struct
import time
import json

server_addr = "localhost"
server_port = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((server_addr, server_port))

ops = ['+', '-', '*', '/']

length_packer = struct.Struct('i')
#print(struct.calcsize('i i c'))
# vagy
# print(packer.size)

nums = random.sample(range(1, 21), 5)
amount = random.randint(1, 10) * 10


msg_bytes = json.dumps(bet).encode("UTF-8")
msg = ":".join([])
sock.sendall(msg)

print(f"Üzenet: {bet}")

msg = sock.recv(length_packer.size)
length, = length_packer.unpack(msg)

msg = sock.recv(length)
result = json.loads(msg.decode("UTF-8"))

print(f"Kapott eredmény: {result}")

sock.close()
