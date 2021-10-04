import socket
#import sys

TCP_IP = 'localhost'
TCP_PORT = 10000
BUFFER_SIZE = 1024
reply = b'Hello kliens'  # reply.encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((TCP_IP, TCP_PORT))

while True:
    try:
        data, claddr = sock.recvfrom(BUFFER_SIZE)
        print(f"Üzenet {claddr}-től: {data.decode()}")
        sock.sendto(reply, claddr)
    except KeyboardInterrupt:
        break

sock.close()
