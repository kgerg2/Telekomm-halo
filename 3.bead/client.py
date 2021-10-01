import socket
import struct
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
format = "1s i"
packer = struct.Struct(format)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))


min_num = 1
max_num = 100
result = None
while result not in [b"K", b"Y", b"V"]:
    if min_num == max_num:
        message = (b"=", min_num)
    else:
        midpoint = (min_num + max_num) // 2
        message = (b">", midpoint)

    sock.send(packer.pack(*message))
    reply = sock.recv(packer.size)
    result, _ = packer.unpack(reply)

    if message[0] == b">":
        if result == b"I":
            min_num = midpoint + 1
        elif result == b"N":
            max_num = midpoint

sock.close()
print(result)