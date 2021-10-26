import socket
import struct
import sys

navi_server_address = ('localhost', 10000)
coords = (int(sys.argv[1]), int(sys.argv[2]))
time = (int(sys.argv[3]), int(sys.argv[4]))
neptun_code = sys.argv[5].encode()

packer = struct.Struct("i i i i 6s")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = packer.pack(*coords, *time, neptun_code)
sock.sendto(msg, navi_server_address)
reply, _ = sock.recvfrom(struct.calcsize("i i"))
sock.close()

print("Idő:", struct.unpack("i i", reply))
