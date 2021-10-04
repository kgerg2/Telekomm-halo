import socket
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
message = b'Hello server!'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.connect((TCP_IP, TCP_PORT))
sock.sendto(message, (TCP_IP, TCP_PORT))
reply, _ = sock.recvfrom(BUFFER_SIZE)
sock.close()

print("Válasz:", reply.decode())
