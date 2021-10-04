from socket import socket, AF_INET, SOCK_STREAM
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)
    
    with open(sys.argv[3], "rb") as f:
        while l := f.read(128):
            client.sendall(l)

print("Elküldtem!")
